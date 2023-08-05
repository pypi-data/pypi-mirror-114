# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golocity', 'golocity.commands']

package_data = \
{'': ['*']}

install_requires = \
['gvmkit-build>=0.2.6,<0.3.0',
 'typer[all]>=0.3.2,<0.4.0',
 'yapapi>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['golocity = golocity.main:golocity']}

setup_kwargs = {
    'name': 'golocity',
    'version': '0.0.1',
    'description': 'An easy to use execution manager for the Golem Network',
    'long_description': "========\nGolocity\n========\n\nSummary\n=======\n\n    Golocity is a young project and while there is testing,\n    there still may be bugs. Be sure and test thoroughly prior to use in a production environment.\n\n**Golocity** is an easy to use CLI execution manager for the Golem Network.\nIt aims to convert and deploy your dockerized project on the Golem Network in\nas little time as possible. It is perfect for developers who want to deploy\ntheir preexisting projects on the Network or those who need a starting point\nto harness all of the Network's features.\n\nInstallation\n============\n\nGolocity is available on ``PyPI``. This will install the latest stable version.\n\nTo install Golocity, simply use ``pip``:\n\n.. code-block:: console\n\n    pip install --user golocity\n\n\nGetting Started\n===============\n\nBuilding the images\n-------------------\n\nBefore your project can be deployed on the Network, we must first build the docker\nimage as well as the Golem virtual machine image. Before issuing the command, make\nsure you have Docker installed and running on your computer.\n\nTo do so, use the ``build`` command:\n\n.. code-block:: console\n\n    golocity build /path/to/your/project\n\nThis will build the requisite images as well as create a ``.golocity``\ndirectory in your projects directory. This directory holds configuration files needed\nby Golocity as well as logs.\n\nThe build command also pushes the Golem virtual machine image to the Network's public\nrepository. To preform a dry-run, append the ``--info`` flag to the command.\n\nUnder the hood, Golocity parses your Dockerfile for ``ENTRYPOINT`` and ``CMD`` commands.\nThese commands currently are not supported in the Golem virtual machine format, so\nGolocity removes them and manually calls them from within the ``deploy`` command. Don't\nworry, Golocity will not alter your project files, it only operates on temporary copies.\n\nDeploying to the Network\n------------------------\n\nOnce you have successfully built and pushed the images, you are ready to deploy your\nproject on the Network! First, make sure you have the ``yagna`` daemon running on your\nmachine, for more information, refer to the `Golem Handbook.\n<https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development/run-first-task-on-golem>`_\n\nNow, deploying is one line away!\n\n.. code-block:: console\n\n    golocity deploy [budget]\n\nReplace ``budget`` with the limit of what to spend while running the project. From here\nGolocity will handle the rest. It will find the best provider and handle the output.\n\nContributing\n=============\n\nPoetry\n------\n\nWe use `poetry <https://github.com/sdispater/poetry>`_ to manage dependencies, to\nget started follow these steps:\n\n.. code-block:: console\n\n    git clone https://github.com/davidstyers/golocity\n    cd golocity\n    poetry install\n    poetry run pytest\n\nPre-Commit\n----------\n\nWe have a configuration for\n`pre-commit <https://github.com/pre-commit/pre-commit>`_ to add the hook run the\nfollowing command:\n\n.. code-block:: console\n\n    pre-commit install\n",
    'author': 'davidstyers',
    'author_email': 'david@styers.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidstyers/golocity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
