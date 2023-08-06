# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_kanban', 'python_kanban.views']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.4,<4.0.0',
 'peewee>=3.14.4,<4.0.0',
 'prompt-toolkit>=3.0.18,<4.0.0']

entry_points = \
{'console_scripts': ['python_kanban = python_kanban.app:run_app']}

setup_kwargs = {
    'name': 'python-kanban',
    'version': '0.1.0',
    'description': 'Text-based interface for a Kanban board in pure Python',
    'long_description': '=============\nPython Kanban\n=============\n\nA terminal-based interface written in pure Python for a very plain Kanban board.\n\nInstallation\n============\n\n.. code:: bash\n\n    pip install python-kanban\n\n\nUsage\n=====\n\nThe simplest way to execute it is to run \n\n.. code:: bash\n\n    python_kanban\n\n\nin the command line. The navigation keys are (or should be) self-explanatory in the\napplication.\n\nThis will create a ``kanban.db`` database file in the current folder. After\nquitting and running ``python_kanban`` again the same database will be loaded\nand the tasks are persisted.\n\nIf you wish to customize the database file or simply manage multiple files, you\ncan set an environment variable with:\n\n.. code:: bash\n\n    export DYNACONF_DB_FILE=another_database_file.db\n\nand it will either create another ``another_database_file.db`` file or load it\nif already existing.\n\nThis is still a work in progress, the looks may be rough in the edges, but most of the main functionality is there already.\n',
    'author': 'Fillipe Goulart',
    'author_email': 'fillipe.gsm@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
