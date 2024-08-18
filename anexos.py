import os
from subprocess import Popen
from hashlib import sha3_224
from glob import glob
import logging
import re

KEY = b'ksP3XsQNrVUZKb62RBCU'
SE_BUCKET = 'jolly-vocal-satyr'
NE_BUCKET = 'openly-brave-falcon'

logging.basicConfig(level=logging.INFO)

for public_path in glob('*/public'):
    if not os.path.isdir(public_path):
        continue

    chall_name = os.path.dirname(public_path)

    uuid = sha3_224(KEY + chall_name.encode('utf-8')).hexdigest()

    tarball = f'{chall_name}_{uuid}.tar.gz'
    tarball_path = os.path.join('anexos', tarball)

    logging.info(f'gerando {tarball}')
    Popen(['tar', '--numeric-owner', '-zcf', tarball_path, public_path]).wait()

    logging.info('uploading to SE')
    Popen(['mgc', 'object-storage', 'objects', 'upload', tarball_path, f'{SE_BUCKET}/{tarball}', '--region=br-se1']).wait()

    logging.info('uploading to NE')
    Popen(['mgc', 'object-storage', 'objects', 'upload', tarball_path, f'{NE_BUCKET}/{tarball}', '--region=br-ne1']).wait()

    se_url = f'https://br-se1.magaluobjects.com/{SE_BUCKET}/{tarball}'
    ne_url = f'https://br-ne1.magaluobjects.com/{NE_BUCKET}/{tarball}'

    readme_file = os.path.join(chall_name, 'README.md')
    with open(readme_file, 'r') as f:
        readme_text = f.read()
    readme_text = re.sub(r'### Anexos[^#]*', f'### Anexos\n\n * [mirror sudeste]({se_url})\n * [mirror nordeste]({ne_url})\n\n', readme_text, flags=re.DOTALL)
    with open(readme_file, 'w') as f:
        f.write(readme_text)
