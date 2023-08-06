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
    'version': '0.2.1',
    'description': 'Make dbt docs and Apache Superset talk to one another',
    'long_description': '# dbt-superset-lineage\n\n<a href="https://github.com/slidoapp/dbt-superset-lineage/blob/main/LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/github/license/slidoapp/dbt-superset-lineage"></a>\n<a href="https://pypi.org/project/dbt-coverage/"><img alt="PyPI" src="https://img.shields.io/pypi/v/dbt-superset-lineage"></a>\n![GitHub last commit](https://img.shields.io/github/last-commit/slidoapp/dbt-superset-lineage)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt-superset-lineage)\n![PyPI - Format](https://img.shields.io/pypi/format/dbt-superset-lineage)\n\n![dbt-superset-lineage](assets/lineage_white.png)\n\n_Make [dbt](https://github.com/dbt-labs/dbt) docs and [Apache Superset](https://github.com/apache/superset) talk to one another_\n\n## Why do I need something like this?\nOdds are rather high that you use dbt together with a visualisation tool. If so, these questions might have popped\ninto your head time to time:\n- "Could I get rid of this model? Does it get used for some dashboards? And in which ones, if yes?"\n- "It would be so handy to see all these well-maintained column descriptions when exploring and creating charts."\n\nIn case your visualisation tool of choice is Supserset, you are in luck!\n\nUsing `dbt-superset-lineage`, you can:\n- Add dependencies of Superset dashboards to your dbt sources and models\n- Sync column descriptions from dbt docs to Superset\n\nThis will help you:\n- Avoid broken dashboards because of deprecated or changed models\n- Choosing the right attributes without navigating back and forth between chart and documentation\n\n## Installation\n\n```\npip install dbt-superset-lineage\n```\n\n## Usage\n`dbt-superset-lineage` comes with two basic commands: `pull-dashboards` and `push-descriptions`.\nThe documentation for the individual commands can be shown by using the `--help` option.\n\nIt includes a wrapper for [Superset API](https://superset.apache.org/docs/rest-api), one only needs to provide\n`SUPERSET_ACCESS_TOKEN`/`SUPERSET_REFRESH_TOKEN` (obtained via `/security/login`)\nas environment variable or through `--superset-access-token`/`superset-refresh-token` option.\n\n**N.B.**\n- Make sure to run `dbt compile` (or `dbt run`) against the production profile, not your development profile  \n- In case more databases are used within dbt and/or Superset and there are duplicate names (`schema + table`) across\n  them, specify the database through `--dbt-db-name` and/or `--superset-db-id` options\n- Currently, `PUT` requests are only supported if CSRF tokens are disabled in Superset (`WTF_CSRF_ENABLED=False`).\n- Tested on dbt v0.20.0 and Apache Superset v1.3.0. Other versions, esp. those newer of Superset, might face errors due\n  to different underlying code and API.\n\n### Pull dashboards\nPull dashboards from Superset and add them as\n[exposures](https://docs.getdbt.com/docs/building-a-dbt-project/exposures/) to dbt docs with\nreferences to dbt sources and models, making them visible both separately and as dependencies.\n\n**N.B.**\n- Only published dashboards are extracted.\n\n```console\n$ cd jaffle_shop\n$ dbt compile  # Compile project to create manifest.json\n$ export SUPERSET_ACCESS_TOKEN=<TOKEN>\n$ dbt-superset-lineage pull-dashboards https://mysuperset.mycompany.com  # Pull dashboards from Superset to /models/exposures/superset_dashboards.yml\n$ dbt docs generate # Generate dbt docs\n$ dbt docs serve # Serve dbt docs\n```\n\n![Separate exposure in dbt docs](assets/exposures_1.png)\n\n![Referenced exposure in dbt docs](assets/exposures_2.png)\n\n### Push descriptions\nPush column descriptions from your dbt docs to Superset as plain text so that they could be viewed\nin Superset when creating charts.\n\n**N.B.**:\n- Run carefully as this rewrites your datasets using merged column metadata from Superset and dbt docs.\n- Descriptions are rendered as plain text, hence no markdown syntax, incl. links, will be displayed.\n- Avoid special characters and strings in your dbt docs, e.g. `→` or `<null>`.\n\n\n```console\n$ cd jaffle_shop\n$ dbt compile  # Compile project to create manifest.json\n$ export SUPERSET_ACCESS_TOKEN=<TOKEN>\n$ dbt-superset-lineage push-descriptions https://mysuperset.mycompany.com  # Push descrptions from dbt docs to Superset\n```\n![Column descriptions in Superset](assets/descriptions.png)\n\n## License\n\nLicensed under the MIT license (see [LICENSE.md](LICENSE.md) file for more details).\n\n\n',
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
