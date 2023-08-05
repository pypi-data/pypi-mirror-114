# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaqti']

package_data = \
{'': ['*']}

install_requires = \
['build>=0.5.1,<0.6.0',
 'click>=8.0.1,<9.0.0',
 'py7zr>=0.16.1,<0.17.0',
 'pytest>=6.2.4,<7.0.0',
 'requests',
 'xmltodict>=0.12.0,<0.13.0',
 'yapf>=0.31.0,<0.32.0']

setup_kwargs = {
    'name': 'yaqti',
    'version': '2021.7.26.8.dev0',
    'description': 'Yet Another QT Installer (ya-q-ti!) - A CLI for installing Qt packages and tooling; for use in enviroments like GitHub Actions or Docker',
    'long_description': '# yaqti (Yet Another QT Installer - ya-q-ti!)\n## overview\n\n\n```bash\npython -m yaqti install \n```\n\n```\npython -m pytest test/\n```\n',
    'author': 'WillBrennan',
    'author_email': 'WillBrennan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willbrennan/yaqti',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
