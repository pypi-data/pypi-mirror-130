# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_superset_lineage']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'pathlib>=1.0.1,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'ruamel.yaml>=0.17.17,<0.18.0',
 'sqlfluff>=0.8.2,<0.9.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['dbt-superset-lineage = '
                     'dbt_superset_lineage.__init__:app']}

setup_kwargs = {
    'name': 'dbt-superset-lineage',
    'version': '0.2.0',
    'description': 'A package for extracting dashboards from Apache Superset to dbt docs as exposures.',
    'long_description': '# dbt-superset-lineage\n\n<a href="https://github.com/slidoapp/dbt-superset-lineage/blob/main/LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/github/license/slidoapp/dbt-superset-lineage"></a>\n<a href="https://pypi.org/project/dbt-coverage/"><img alt="PyPI" src="https://img.shields.io/pypi/v/dbt-superset-lineage"></a>\n<a href="https://pepy.tech/project/dbt-superset-lineage"><img alt="Downloads" src="https://pepy.tech/badge/dbt-superset-lineage"></a>\n![GitHub last commit](https://img.shields.io/github/last-commit/slidoapp/dbt-superset-lineage)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt-superset-lineage)\n![PyPI - Format](https://img.shields.io/pypi/format/dbt-superset-lineage)\n\nA CLI library with Python backend for extracting dashboards from Apache Superset to dbt docs as exposures.\n\n## Installation\n\n```\npip install dbt-superset-lineage\n```\n\n## License\n\nLicensed under the MIT license (see [LICENSE.md](LICENSE.md) file for more details).\n\n\n',
    'author': 'Michal Kolacek',
    'author_email': 'mkolacek@slido.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/slidoapp/dbt-superset-lineage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
