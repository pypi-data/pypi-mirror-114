# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convbot']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0', 'transformers>=4.9.0,<5.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "4.0" and sys_platform == "linux"': ['torch>=1.9.0,<2.0.0']}

setup_kwargs = {
    'name': 'convbot',
    'version': '0.1.0',
    'description': 'pack_name descr ',
    'long_description': '# convbot\n[![tests](https://github.com/ffreemt/convbot/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/convbot/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/convbot.svg)](https://badge.fury.io/py/convbot)\n\nA conversational bot based on huggingface transformers\n\n## Install it\n\n```shell\npip install convbot\n# or poetry add convbot\n# pip install git+htts://github.com/ffreemt/convbot\n# poetry add git+htts://github.com/ffreemt/convbot\n\n# To upgrade\npip install convbot -U\n# or poetry add convbot@latest\n```\n\n## Use it\n```python\nfrom convbot import convbot\n\nprin(convertbot("How are you?"))\n# I am good  # or along that line\n```\n\nInteractive\n\n```bash\npython -m convbot\n```\n## Not tested in Windows 10 and Mac\n\nThe module uses pytorch that is installed differently in Windows than in Linux. To run in Windows or Mac, you can probably just try to install pytorch manually.\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/convbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
