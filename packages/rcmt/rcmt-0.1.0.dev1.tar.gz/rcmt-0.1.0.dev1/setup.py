# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcmt', 'rcmt.source']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'mergedeep>=1.3.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'structlog>=21.1.0,<22.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['rcmt = rcmt.cli:main']}

setup_kwargs = {
    'name': 'rcmt',
    'version': '0.1.0.dev1',
    'description': '',
    'long_description': '# rcmt\n\n- Ensure that files look the same across repositories.\n- Merge global settings with user-configured settings in each repository.\n',
    'author': 'Markus Meyer',
    'author_email': 'hydrantanderwand@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wndhydrnt/rcmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
