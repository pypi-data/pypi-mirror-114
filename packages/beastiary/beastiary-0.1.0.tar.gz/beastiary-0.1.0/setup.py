# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beastiary']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['beastiary = beastiary.main:app']}

setup_kwargs = {
    'name': 'beastiary',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Beastiary\nThis is a replacement for tracer. It's feature feature is the real time aspect. Secondly it's modern looking. 3rd it has improved features. \n\n\n## CLI\nLaunch the app\nCan point to log file to autostart watcher\n\n## Webapp \nVue\nPlotly\n\n## Web API\nFastAPI that sends data to and from DB and servers the webapp\nCan start file watchers\n\n## Watcher \nPython class that watches files and updates DB with changes.\n\n\n## BD (MEMORY)\nProtected by the CRUD\n\n\n## distribution \nCLI vs app (just launches web browser)\nhttps://docs.python-guide.org/shipping/freezing/",
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
