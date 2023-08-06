# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['togpush']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'pandas==1.3.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.46.0,<5.0.0']

entry_points = \
{'console_scripts': ['fsm = togpush.fsm:main', 'tog = togpush.tog:main']}

setup_kwargs = {
    'name': 'togpush',
    'version': '1.1.12',
    'description': 'Command Line Interface for fetching data from fsm and pushing to tog for tagging',
    'long_description': None,
    'author': 'Lohith Anandan',
    'author_email': 'lohith@vernacular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
