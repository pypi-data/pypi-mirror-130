# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pypus']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'requests>=2.25.1,<3.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['pypus = pypus.cli:main']}

setup_kwargs = {
    'name': 'pypus',
    'version': '1.1.0',
    'description': 'Octopus cli toolkit',
    'long_description': '# Pypus\n\nPypus is a cli tool for publishing Octopus Deploy Runbooks.\n\n## Install\n\n```bash\n$ pip install pypus\n```\n',
    'author': 'Michael MacKenna',
    'author_email': 'mmackenna@unitedfiregroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
