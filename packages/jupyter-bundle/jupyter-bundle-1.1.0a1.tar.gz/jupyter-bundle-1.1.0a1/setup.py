# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyterbundle', 'jupyterbundle.widgets']

package_data = \
{'': ['*'], 'jupyterbundle': ['_config/*']}

install_requires = \
['daipe-core>=1.1,<2.0',
 'ipywidgets>=7.6',
 'jupyterlab>=3.0.0',
 'jupytext>=1.11.0',
 'pyfony-core>=0.8.0,<0.9.0']

entry_points = \
{'pyfony.bundle': ['create = jupyterbundle.JupyterBundle:JupyterBundle']}

setup_kwargs = {
    'name': 'jupyter-bundle',
    'version': '1.1.0a1',
    'description': 'Jupyter Lab support for Daipe',
    'long_description': '# Jupyter Bundle\n\nAdditional component of the [Daipe Framework](https://www.daipe.ai).  \n\n## Resources\n\n* [Documentation](https://docs.daipe.ai/)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/jupyter-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
