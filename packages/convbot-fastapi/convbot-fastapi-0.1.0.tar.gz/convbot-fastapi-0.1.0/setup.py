# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convbot_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'logzero>=1.7.0,<2.0.0',
 'pydantic[dotenv]>=1.8.1,<2.0.0',
 'transformers>=4.9.0,<5.0.0',
 'uvicorn>=0.14.0,<0.15.0']

extras_require = \
{':python_version >= "3.7" and python_version < "4.0" and sys_platform == "linux"': ['torch>=1.9.0,<2.0.0']}

setup_kwargs = {
    'name': 'convbot-fastapi',
    'version': '0.1.0',
    'description': 'Convbot with fastapi',
    'long_description': '# convbot-fastapi\n[![tests](https://github.com/ffreemt/convbot-fastapi/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/convbot_fastapi/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/convbot_fastapi.svg)](https://badge.fury.io/py/convbot_fastapi)\n\nconvbot-fastapi descr\n\n## Install it\n\n```shell\npip install convbot-fastapi\n# or poetry add convbot-fastapi\n# pip install git+htts://github.com/ffreemt/convbot-fastapi\n# poetry add git+htts://github.com/ffreemt/convbot-fastapi\n\n# To upgrade\npip install convbot-fastapi -U\n# or poetry add convbot-fastapi@latest\n```\n\n## Use it\n```bash\npython -m convbot_fastapi\n```\nPoint your browser to `httpL//127.0.0.1:8000/docs`\n\nOr with uvicorn\n```bash\nuvicorn convbot_fastapi.convbot_fastapi:app\n```\n\n## Deploy it to the cloud\nClone the repo\n```bash\ngit clone https://github.com/ffreemt/convbot-fastapi\ncd convbot-fastapi\n```\n\nCreate a docker image from `Dockerfile` and upload it to `https://hub.docker.com/`\n\nSign up and deploy the docker image to, for example, `koyeb.com`.\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/convbot-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
