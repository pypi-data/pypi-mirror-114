# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cml']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.9.0,<3.0.0',
 'httpx==0.18.2',
 'requests==2.25.1',
 'tqdm==4.61.2',
 'typer[all]>=0.3.2,<0.4.0',
 'ujson==4.0.2']

entry_points = \
{'console_scripts': ['cml = cml.cml:app']}

setup_kwargs = {
    'name': 'chanml-client',
    'version': '0.1.1',
    'description': 'chanml-client',
    'long_description': '# ChanML\n\n ## Instalation\n\n    * poetry installation\n    ',
    'author': 'Jun Du',
    'author_email': 'dujun@ruiking.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
