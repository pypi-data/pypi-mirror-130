# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_converter_valtensir']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'csv_converter_valtensir.converter:converter']}

setup_kwargs = {
    'name': 'csv-converter-valtensir',
    'version': '0.1.2',
    'description': 'A project to converter JSON to CSV and CSV to JSON files.',
    'long_description': "# A  CSV <> JSON converter\n\nA CSV to JSON and JSON to CSV converter.\n\n## Introduction\n\nA project to learning porpuses. \n\n## What this project can do\n\n1 - Read a csv file or a folder with csv's and convert them to JSON.\n\n2 - Read a json file or a folder with json's and convert them to CSV.\n\nThis project is a program running on terminal, preferably install with pipx:\n\n```bash\npipx install csv_converter_valtensir\n```\n\n## Help\n```bash\nUsage: csv_converter [OPTIONS]\n\nOptions:\n  -c, --convert TEXT    Format you want to convert. cc -> Convert CSV to JSON;\n                        cj -> Convert JSON to CSV.\n  -i, --input TEXT      Path where to find the files to convert.\n  -o, --output TEXT     Path where the converted files will be saved.\n  -d, --delimiter TEXT  Separator used to split the files.\n  -p, --prefix TEXT     Prefix used to prepend to the name of the converted\n                        file saved on disk.The suffix will be a number\n                        starting from 0. ge: file_0\n  --help                Show this message and exit.\n\n```",
    'author': 'Valtensir Lopes',
    'author_email': 'valtensirl@gmail.com',
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
