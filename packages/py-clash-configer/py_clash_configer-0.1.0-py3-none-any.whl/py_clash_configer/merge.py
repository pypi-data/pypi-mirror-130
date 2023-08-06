from io import StringIO

import requests
import yaml

from .log import logger

L = logger.getChild(__name__)


def download(url: str):
    L.debug('downloading from: %s', url)
    with requests.get(url) as resp:
        if not resp.ok:
            raise ValueError('cannot download yaml from %s' % (url,))
        if 'yaml' not in resp.headers['content-type'].lower():
            L.debug(resp.text)
            raise ValueError('downloaded content is not a YAML config')
        return resp.text


def patch_yaml(f1, f2):
    y1 = yaml.safe_load(f1)
    y2 = yaml.safe_load(f2)
    # TODO replace shallow merge with rule-based merge
    y1.update(y2)
    return yaml.safe_dump(y1, encoding='utf-8')


def update(url, patch, out):
    config = download(url)
    if patch:
        subscription = StringIO(config)
        L.debug('patch with %s', patch)
        with open(patch) as local, open(out, 'wb') as outf:
            L.debug('save to %s', out)
            outf.write(patch_yaml(subscription, local))
    else:
        with open(out, 'w', encoding='utf-8') as outf:
            L.debug('save original file to %s', out)
            outf.write(config)
