# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_json_converter_mtba']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_json_converter = '
                     'csv_json_converter_mtba.converter:converter']}

setup_kwargs = {
    'name': 'csv-json-converter-mtba',
    'version': '0.1.0',
    'description': 'Conversor CSV-JSON',
    'long_description': "# CSV-JSON Converter\n\nCSV to JSON converter.\n\n## Introduction\n\nTrabalho desenvolvido para a disciplina Python para Ciência de Dados do curso de pós-graduação em Ciência de Dados e Big Data da PUC Minas - 2021.\n\n### What this project can do\n\nRead a **csv/json** file or a **folder** with csv/json's and convert them to **json/csv**.\nThis project is a program running on terminal, preferably install with pipx:\n\n```bash\npipx install csv_json_converter_mtba\n```\n\nTo use, just type in:\n\n```bash\ncsv_json_converter --help\n```\n\nThis will list all available options.",
    'author': 'Marco Andrade',
    'author_email': 'marcotbandrade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
