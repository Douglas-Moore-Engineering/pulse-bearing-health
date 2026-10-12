"""Package a private Docker archive and manifests without pushing or deploying."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import yaml

from render_single_node_manifests import render


def docker(*args):
    result = subprocess.run(['docker', *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--identity-config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pilot-components', action='store_true')
    args = parser.parse_args()
    identity = json.loads(args.identity_config.read_text(encoding='utf-8'))
    image_id = docker('image', 'inspect', args.image, '--format', '{{.Id}}')
    image_tag = 'pulse-api:sha256-'+image_id.removeprefix('sha256:')
    documents = render(image_tag, **identity, pilot_components=args.pilot_components)
    args.output.mkdir(parents=True, exist_ok=False)
    docker('tag', args.image, image_tag)
    archive = args.output/'pulse-api.tar'
    docker('save', '--output', str(archive), image_tag)
    manifests = args.output/'application.yaml'
    manifests.write_text(yaml.safe_dump_all(documents, sort_keys=False), encoding='utf-8')
    release = {'imageId': image_id, 'imageTag': image_tag,
               'archiveSha256': sha256(archive), 'manifestsSha256': sha256(manifests),
               'scope': 'single-node reference; qualified alerts unavailable',
               'cloudDeployed': False, 'serverSideValidated': False}
    (args.output/'release.json').write_text(json.dumps(release, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(release))
