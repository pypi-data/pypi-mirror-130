# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['puc_lpgomes_csvconverter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'puc_lpgomes_csvconverter.converter:converter']}

setup_kwargs = {
    'name': 'puc-lpgomes-csvconverter',
    'version': '0.1.4',
    'description': 'Convert CSV to Json. For only purpose at PUC Python Class',
    'long_description': '# File Converter\n\nCSV to JSON and JSON to CSV converter.\n\n## Introduction\n\nStudying how to deploy a lib on PyPi at PUC using Poetry.\n\n### What this project can do\n\nRead a **csv** or **json** files or a **folders** with files and convert them to **JSON** or **CSV**.\nThis project is a program running on terminal, preferably install with pipx:\n\n\n```bash\npipx install puc_lpgomes_csvconverter\n```\n\nTo use, just type in:\n\n```bash\ncsv_converter --help\n```\n\nThis will list all available options.\n',
    'author': 'Leandro P. Gomes',
    'author_email': 'leandropgomes11@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
