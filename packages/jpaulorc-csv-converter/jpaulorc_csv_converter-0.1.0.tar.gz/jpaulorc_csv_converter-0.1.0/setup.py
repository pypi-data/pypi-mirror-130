# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jpaulorc_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'jpaulorc_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'jpaulorc-csv-converter',
    'version': '0.1.0',
    'description': 'Convert csv to json and json to csv. Publishin only for leaning purposes.',
    'long_description': '# File Converter\n\nUsed to convert files to CSV or JSON.\n\n## Introduction\n\nLearning how to deploy a lib on PyPi at PUC using Poetry.\n\n\n\n### What this project can do\n\nRead a **CSV** or **JSON** file or a **folder** with files and convert them to **CSV** or **JSON**.\n\n - If the file was a **CSV** then it will be converted to **JSON**.\n - If the file was a **JSON** then it will be converted to **CSV**.\n\nThis project is a program running on terminal, preferably install with pipx:\n\n\n```bash\npipx install jpaulorc-csv-converter\n```\n\nTo use, just type in:\n\n```bash\ncsv_converter --help\n```\n\nThis will list all available options.',
    'author': 'Joao Corte',
    'author_email': 'jpaulorc@gmail.com',
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
