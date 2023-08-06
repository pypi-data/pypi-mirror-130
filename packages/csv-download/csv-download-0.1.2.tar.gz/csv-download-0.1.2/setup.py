# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['csv_download']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['csv_download = csv_download.main:cli']}

setup_kwargs = {
    'name': 'csv-download',
    'version': '0.1.2',
    'description': 'Script to specify the column with URL in csv and download and save in bulk.',
    'long_description': '# csv_download\nScript to specify the column with URL in csv and download and save in bulk\n\n\n## usage\n\n`csv_download` reads csv and downloads the URLs of the specified columns in sequence.\nYou can see the available options with `-h`\n```shell\n$ csv_download -h\n\nusage: csv_download [-h] [-o OUT_PATH] [-p PREFIX] [-t TARGET_URL_COLUM] [-n NAME_COLUM] [--sleep SLEEP] [--header-skip] file path\n\npositional arguments:\n   file path\n\noptional arguments:\n   -h, --help show this help message and exit\n   -o OUT_PATH, --out OUT_PATH\n   -p PREFIX, --prefix PREFIX\n   -t TARGET_URL_COLUM, --target-url-col TARGET_URL_COLUM\n   -n NAME_COLUM, --name-col NAME_COLUM\n   --sleep SLEEP\n   --header-skip\n```\n\n### example\n```shell\n$ csv_download ./example/example.csv -o ./image -p example --header-skip\n```\n\n## Author\n[Godan] (https://github.com/godan)\n\n\n\nTranslated with Google Translate',
    'author': 'godan',
    'author_email': 'shogo070920@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Godan/csv_download',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
