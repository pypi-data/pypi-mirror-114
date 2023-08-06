# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jbtuner2_manager']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['jbt2 = jbtuner2_manager.main:app']}

setup_kwargs = {
    'name': 'jbtuner2-manager',
    'version': '0.1.5',
    'description': 'An integrated tool for managing ChordX JBTuner2',
    'long_description': '',
    'author': 'Ying Shaodong',
    'author_email': 'gavin.ying@chordx.co',
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
