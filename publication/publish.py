"""Publish only reviewed binary deliveries from a temporary public branch.

No private source or credential is copied. Input bytes are checked before writes.
The existing catalogue generator remains responsible for ten-version retention.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = 'sdebliquy35-source/TRAPS-distribution'
API = 'https://api.github.com/repos/' + REPO


def assemble(item, folder):
    name = item['file']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+\.(apk|exe|pdf)', name):
        raise ValueError('Unexpected delivery filename')
    target = folder / name
    with target.open('wb') as output:
        for part in item['parts']:
            if not re.fullmatch(r'publication/parts/[a-z0-9_.-]+', part):
                raise ValueError('Unexpected part path')
            output.write(Path(part).read_bytes())
    raw = target.read_bytes()
    if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
        raise ValueError('Delivery bytes do not match the reviewed manifest')
    expected = b'PK' if name.endswith('.apk') else b'MZ' if name.endswith('.exe') else b'%PDF-'
    if not raw.startswith(expected):
        raise ValueError('Unexpected delivery format')
    return target


def run(manifest, verify_only=False):
    folder = Path('publication-ready')
    folder.mkdir(exist_ok=True)
    if manifest.get('schema') != 1:
        raise ValueError('Unknown manifest schema')
    releases = manifest['releases']
    tags = {r['app'] + '-' + str(r['build']) for r in releases}
    if tags != {'traps-126', 'jugement-97'} or len(releases) != 2:
        raise ValueError('Only the explicitly requested official releases are allowed')
    # Complete every byte check before creating any public release.
    for item in releases + manifest['guides']:
        assemble(item, folder)
    for release in releases:
        metadata = release['metadata']
        if any(metadata[k] != release[k] for k in ('app', 'build', 'file', 'version', 'sha256')):
            raise ValueError('Release metadata differs from the reviewed file')
    if verify_only:
        print('All reviewed binary deliveries verified; no network operation.')
        return
    if os.environ.get('GITHUB_REPOSITORY') != REPO:
        raise ValueError('Publication is restricted to the public download repository')
    headers = {'Authorization': 'Bearer ' + os.environ['GITHUB_TOKEN'],
               'Accept': 'application/vnd.github+json', 'User-Agent': 'TRAPS-reviewed-release'}

    def request(path, method='GET', value=None, raw=None, content_type=None):
        url = path if path.startswith('https://uploads.github.com/') else API + path
        h = dict(headers)
        if value is not None:
            raw = json.dumps(value).encode()
            h['Content-Type'] = 'application/json'
        if content_type:
            h['Content-Type'] = content_type
        with urllib.request.urlopen(urllib.request.Request(url, data=raw, headers=h, method=method), timeout=180) as response:
            data = response.read()
            return json.loads(data) if data else None

    for release in releases:
        tag = release['app'] + '-' + str(release['build'])
        try:
            state = request('/releases/tags/' + tag)
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
            state = request('/releases', 'POST', dict(tag_name=tag, name=release['title'],
                            body=release['notes'], draft=True, prerelease=False))
        upload = state['upload_url'].split('{')[0]
        if urllib.parse.urlparse(upload).hostname != 'uploads.github.com':
            raise ValueError('Unexpected upload host')
        payloads = [(release['file'], (folder / release['file']).read_bytes()),
                    ('release.json', (json.dumps(release['metadata'], indent=2) + '\n').encode())]
        for name, content in payloads:
            assets = request('/releases/' + str(state['id']) + '/assets')
            old = next((a for a in assets if a['name'] == name), None)
            digest = 'sha256:' + hashlib.sha256(content).hexdigest()
            if old:
                if old.get('digest') != digest or old['size'] != len(content):
                    raise ValueError('An existing release asset differs; it is not overwritten')
            else:
                created = request(upload + '?name=' + urllib.parse.quote(name), 'POST', raw=content,
                                  content_type='application/octet-stream')
                if created.get('digest') != digest or created['size'] != len(content):
                    raise ValueError('Uploaded asset digest differs')
        request('/releases/' + str(state['id']), 'PATCH', dict(name=release['title'], body=release['notes'],
                draft=False, prerelease=False, make_latest='true'))
        print('Published official release:', tag)

    # Update only the public PDFs and public download instructions on main.
    head = request('/git/ref/heads/main')['object']['sha']
    tree = request('/git/commits/' + head)['tree']['sha']
    entries = []
    for guide in manifest['guides']:
        blob = request('/git/blobs', 'POST', dict(encoding='base64', content=base64.b64encode((folder / guide['file']).read_bytes()).decode()))
        entries.append(dict(path='guides/' + guide['file'], mode='100644', type='blob', sha=blob['sha']))
    entries.append(dict(path='README.md', mode='100644', type='blob', content=manifest['readme']))
    updated = request('/git/trees', 'POST', dict(base_tree=tree, tree=entries))
    commit = request('/git/commits', 'POST', dict(message='Versions officielles0.97/APK126 et guides utilisateurs actualisés',
                     tree=updated['sha'], parents=[head]))
    request('/git/refs/heads/main', 'PATCH', dict(sha=commit['sha'], force=False))
    # A GITHUB_TOKEN publication does not trigger another release workflow.
    subprocess.run([sys.executable, '.github/catalog.py'], check=True)
    branch = os.environ.get('GITHUB_REF_NAME', '')
    if branch == 'publication/officielle-097-126':
        request('/git/refs/heads/' + branch, 'DELETE')
    print('Public guides and catalogue updated; temporary upload branch removed.')


if __name__ == '__main__':
    run(json.loads(Path('publication/manifest.json').read_text()), '--verify-only' in sys.argv)
