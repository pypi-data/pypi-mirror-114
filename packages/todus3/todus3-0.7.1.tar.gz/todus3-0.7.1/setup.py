# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todus3']

package_data = \
{'': ['*']}

install_requires = \
['multivolumefile>=0.2.3,<0.3.0',
 'py7zr>=0.16.1,<0.17.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.61.2,<5.0.0']

entry_points = \
{'console_scripts': ['todus3 = todus3.main:main']}

setup_kwargs = {
    'name': 'todus3',
    'version': '0.7.1',
    'description': 'ToDus client for S3',
    'long_description': '# ToDus client for S3\n\n[![](https://img.shields.io/pypi/v/todus3.svg)](https://pypi.org/project/todus3)\n[![](https://img.shields.io/pypi/pyversions/todus3.svg)](\nhttps://pypi.org/project/todus3)\n[![Downloads](https://pepy.tech/badge/todus3)](https://pepy.tech/project/todus3)\n[![](https://img.shields.io/pypi/l/todus3.svg)](https://pypi.org/project/todus3)\n[![CI](https://github.com/oleksis/todus/actions/workflows/python-ci.yml/badge.svg)](https://github.com/oleksis/todus/actions/workflows/python-ci.yml)\n[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nUse the ToDus API (login/download/upload) in your Python projects.\n\n## Install\n\nTo install run\n```bash\n  pip install todus3\n```\n\n## Usage\n```bash\n### Help\ntodus3 -- help\n\n### Login and Enter PIN\ntodus3 -n 53123456 login\n\n### Download from TXT files with 3 Workers/Threads\ntodus3 -n 53123456 download -t 3 file.txt [file.txt ...]\n\n### Upload file by parts in Bytes (10 MB)\ntodus3 -n 53123456 upload binary.bin -p 10485760\n```\n',
    'author': 'adbenitez',
    'author_email': 'adbenitez@nauta.cu',
    'maintainer': 'Oleksis Fraga',
    'maintainer_email': 'oleksis.fraga@gmail.com',
    'url': 'https://github.com/oleksis/todus/tree/todus3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
