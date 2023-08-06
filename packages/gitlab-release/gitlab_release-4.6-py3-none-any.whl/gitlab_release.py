#!/usr/bin/env python3

import os
import io
import re
import json
import codecs
import zipfile
import argparse
import itertools
import mimetypes
import urllib.error
from glob import glob
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit, urlencode, quote
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        # self.boundary = mimetools.choose_boundary()
        self.boundary = '----------lImIt_of_THE_fIle_eW_$'
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return

    def get_binary(self):
        """Return a binary buffer containing the form data, including attached files."""
        def to_bytes(s):
            return s.encode('ascii') if isinstance(s, str) else s

        part_boundary = '--' + self.boundary

        binary = io.BytesIO()
        needsCLRF = False
        # Add the form fields
        for name, value in self.form_fields:
            if needsCLRF:
                binary.write('\r\n')
            needsCLRF = True

            block = [part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value
            ]
            binary.write('\r\n'.join(block))

        # Add the files to upload
        for field_name, filename, content_type, body in self.files:
            if needsCLRF:
                binary.write('\r\n')
            needsCLRF = True

            block = [part_boundary,
              str('Content-Disposition: file; name="%s"; filename="%s"' % \
              (field_name, filename)),
              'Content-Type: %s' % content_type,
              ''
              ]
            binary.write(b'\r\n'.join([to_bytes(s) for s in block]))
            binary.write(b'\r\n')
            binary.write(to_bytes(body))

        # add closing boundary marker,
        binary.write(to_bytes('\r\n--' + self.boundary + '--\r\n'))
        return binary


def url_server_path(url):
    scheme, netloc, path, query, fragment = urlsplit(url)
    return f"{scheme}{netloc}", f"{path}{query}{fragment}"


def main():
    parser = argparse.ArgumentParser(description='Upload files to gitlab tag (release)')
    parser.add_argument('--server', default=urljoin(os.environ.get('CI_PROJECT_URL'), '/'),
                        help='url of gitlab server (default: $CI_PROJECT_URL)')
    parser.add_argument('--project_id', default=os.environ.get('CI_PROJECT_ID'),
                        help='Unique id of project, available in '
                             'Project Settings/General (default: $CI_PROJECT_ID)')
    parser.add_argument('--release_tag', default=os.environ.get('CI_COMMIT_TAG'),
                        help='Tag to upload files against (default: $CI_COMMIT_TAG)')
    parser.add_argument('--timeout', type=int, default=120, help='Timeout for http requests')
    parser.add_argument('--ignore_cert', action="store_true", help='Ignore ssl certificate failures')

    parser.add_argument('--job-id', default=os.environ.get('CI_JOB_ID', 0), help='Override the job number used for artifacts')
    parser.add_argument('--artifact-zip', action="store_true", help='Link artifacts zip from current job')

    parser.add_argument('--zip', help='Add all files to provided zip name and upload that')
    parser.add_argument('--description', default='', help='Release description to be put in front of the files')
    parser.add_argument('--link-prefix', default='', help='Prefix text added in front of each file link, eg "* " to create a list')
    parser.add_argument('--link-type', default='package', help='The type of the link: other, runbook, image, package')
    parser.add_argument('--link-in-desc', action="store_true", help='Add the artifact links to the description. Uses release asset otherwise')

    parser.add_argument('--link-artifact', action="store_true", help='Link files as artifact from the current job')

    parser.add_argument('--private-token', default=os.environ.get('PRIVATE_TOKEN', ""), help='login token with permissions to commit to repo')

    parser.add_argument('--create-tag', action="store_true", help="create the tag if it doesn't already exist")
    parser.add_argument('files', nargs="*", help='glob/s of files to upload')

    args = parser.parse_args()

    server = args.server
    if not server or server == '/':
        raise SystemExit("Must provide --server if not running from CI (hence without env var 'CI_PROJECT_URL')")

    project_id = args.project_id
    if not project_id:
        raise SystemExit("Must provide --project_id if not running from CI (hence without env var 'CI_PROJECT_ID')")
    project_id = quote(project_id, safe='')

    release_tag = args.release_tag
    if not release_tag:
        raise SystemExit("Must provide --release_tag if not running from CI (hence without env var 'CI_COMMIT_TAG')")

    verify = not args.ignore_cert

    print("Uploading to %s (id: %s) @ %s" % (server, project_id, release_tag))

    if not server.endswith('/'):
        server += '/'

    api_url = f"{server}api/v4/projects/{project_id}/"

    link_in_desc = args.link_in_desc or args.link_prefix

    uploads = []
    assets = []

    if args.description:
        uploads.append(args.description)

    all_files = list(itertools.chain(*[glob(f.replace('\\', '/')) if '*' in f else [f] for f in args.files]))

    if not (all_files or args.artifact_zip or args.link_artifact):
        raise SystemExit("No files found for %s" % args.files)

    token = os.environ.get('CI_JOB_TOKEN')

    private_token = args.private_token

    if all_files and not private_token and not token:
        if re.match(r'[A-Za-z0-9]', all_files[0]):
            print("WARNING: legacy use of PRIVATE_TOKEN as first positional argument detected or token not supplied, please see `gitlab_release --help`")
            private_token = all_files[0]
            all_files = all_files[1:]

    if all_files and private_token == all_files[0]:
        print("WARNING: legacy use of PRIVATE_TOKEN as first positional argument detected, please see `gitlab_release --help`")
        all_files = all_files[1:]

    if private_token:
        auth = {'PRIVATE-TOKEN': private_token}
    elif token:
        print("Using CI_JOB_TOKEN for auth")
        auth = {'JOB-TOKEN': token}
        if not args.link_artifact:
            raise SystemExit("File upload not available with CI_JOB_TOKEN, must use 'PRIVATE_TOKEN'")
    else:
        raise SystemExit("Neither PRIVATE_TOKEN nor CI_JOB_TOKEN available, must be in env var 'PRIVATE_TOKEN' or provided as arg with --private-token")

    artifact_job = args.job_id
    if args.artifact_zip or args.link_artifact:
        if not artifact_job:
            print("Must provide --artifact-job <id> for artifact files")
            exit(-1)

        if args.link_artifact:
            for fname in all_files:
                if fname.startswith('./'):
                    fname = fname[2:]
                url = api_url + "jobs/%s/artifacts/%s" % (artifact_job, fname)

                if link_in_desc:
                    uploads.append(
                        "%s[%s](%s)" % (args.link_prefix, fname, url)
                    )
                else:
                    assets.append((fname, url))

        if args.artifact_zip:
            url = api_url + "jobs/%s/artifacts" % artifact_job
            fname = "artifact.zip"  # todo find a better name automatically?

            if link_in_desc:
                uploads.append(
                    "%s[%s](%s)" % (args.link_prefix, fname, url)
                )
            else:
                assets.append((fname, url))

    if args.zip:
        with zipfile.ZipFile(args.zip, "w", zipfile.ZIP_DEFLATED) as zf:
            def zipdir(path, ziph):
                # ziph is zipfile handle
                for root, dirs, files in os.walk(path):
                    for file in files:
                        ziph.write(os.path.join(root, file))

            for fname in all_files:
                print (fname)
                if fname == args.zip:
                    continue
                if os.path.isdir(fname):
                    zipdir(fname, zf)
                else:
                    zf.write(fname)

        all_files = [os.path.abspath(args.zip)]

    rsp = requests.get(api_url, headers=auth, verify=verify)
    try:
        rsp.raise_for_status()
    except Exception as ex:
        raise SystemExit("Obtaining project info failed: {ex}".format(ex=ex))
    else:
        response = rsp.json()
        project_base_url = response['web_url']

    if all_files and not args.link_artifact:
        print("Uploading %s" % all_files)

        for fname in all_files:

            with codecs.open(fname, 'rb') as filehandle:
                rsp = requests.post(api_url + 'uploads', files={'file': filehandle}, headers=auth, verify=verify)
                try:
                    rsp.raise_for_status()
                except Exception as ex:
                    raise SystemExit("Upload of {f} failed: {ex}".format(f=fname, ex=ex))
                else:
                    response = rsp.json()
                    if link_in_desc:
                        uploads.append(
                            "%s%s" % (args.link_prefix, response['markdown'])
                        )
                    else:
                        assets.append((response['alt'], project_base_url + response['url']))

    def fix_markdown(match):
        return "[%s](%s)" % (match.group(1), quote(match.group(2), safe='/:'))

    uploads = [re.sub(r'^\[(.*)\]\((.*)\)$', fix_markdown, u) for u in uploads]

    description = '  \n'.join(uploads)

    # Now we've got the uploaded file info, attach that to the tag
    tag_url = urljoin(api_url, 'repository/tags/{t}'.format(t=quote(release_tag, safe='')))
    try:
        tag_details = requests.get(tag_url, headers=auth, verify=verify).json()
    except Exception as ex:
        tag_details = None

    if tag_details is None or '404' in tag_details['message']:
        if args.create_tag:
            default_branch = requests.get(api_url, headers=auth, verify=verify).json().get('default_branch', 'master')
            url = api_url + 'repository/tags?tag_name={t}&ref={r}'.format(
                t=quote(release_tag, safe=''), r=quote(default_branch, safe='')
            )
            tag_details = requests.post(url, headers=auth, verify=verify).json()
        else:
            raise SystemExit("Tag not found:", release_tag)

    method = requests.post
    release_exists = False
    if link_in_desc and 'release' in tag_details and tag_details['release'] is not None:
        print('Update existing release')
        description = '  \n'.join((tag_details['release']['description'], description))
        method = requests.put
        release_exists = True

    data = {'tag_name': release_tag, 'description': description}

    if not link_in_desc:
        rsp = requests.get(api_url + 'releases/' + release_tag, headers=auth, verify=verify)
        if rsp.status_code == 200:
            release_exists = True

        data["assets"] = dict(
                links=[
                    dict(name=name, url=url, link_type=args.link_type) for name, url in assets
                ]
            )

    try:
        if link_in_desc:
            # Update the existing release description
            rsp = method(api_url + 'releases/' + release_tag, data={'description': description}, headers=auth, verify=verify)
            rsp.raise_for_status()
        else:
            if release_exists:
                # Add new assets
                for link in data["assets"]['links']:
                    rsp = requests.post(api_url + 'releases/' + release_tag + '/assets/links', headers=auth, verify=verify, data=link)
                    rsp.raise_for_status()
            else:
                # Create new release
                rsp = method(api_url + 'releases', json=data, headers=auth, verify=verify)
                rsp.raise_for_status()

        tagname = rsp.json().get('tag_name', release_tag)
        print("Uploaded %s to tag %s: %s" % (all_files, tagname, project_base_url + "/tags/%s" % quote(tagname)))

    except Exception as ex:
        raise SystemExit("Uploading release failed: {f}, error: {ex}".format(f=all_files, ex=ex))


if __name__ == '__main__':
    main()
