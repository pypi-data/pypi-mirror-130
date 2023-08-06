# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leapcli', 'leapcli.dataset']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.18',
 'docopt==0.6.2',
 'luddite==1.0.2',
 'pytest-mock==3.6.1',
 'python-json-logger==2.0.2',
 'requests==2.26.0',
 'semver>=2.13.0,<3.0.0',
 'tensorleap-openapi-client==1.1.4',
 'toml==0.10.2']

entry_points = \
{'console_scripts': ['leap = cli:__main__']}

setup_kwargs = {
    'name': 'leapcli',
    'version': '0.1.19',
    'description': 'Tensorleap CLI',
    'long_description': None,
    'author': 'Assaf Lavie',
    'author_email': 'assaf.lavie@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensorleap/cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
