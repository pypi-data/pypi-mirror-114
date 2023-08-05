# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remarking',
 'remarking.cli',
 'remarking.cli.commands',
 'remarking.highlight_extractor',
 'remarking.storage']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.20,<2.0.0',
 'click-help-colors>=0.9.1,<0.10.0',
 'click>=8.0.1,<9.0.0',
 'halo>=0.0.31,<0.0.32',
 'python-dateutil>=2.8.1,<3.0.0',
 'rmapy==0.3.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'docs': ['Sphinx>=4.1.1,<5.0.0', 'furo>=2021.7.5-beta.38,<2022.0.0']}

entry_points = \
{'console_scripts': ['remarking = remarking.cli.cli:command_line']}

setup_kwargs = {
    'name': 'remarking',
    'version': '0.1.3',
    'description': 'Extract highlights from your ReMarkable tablet.',
    'long_description': '<h1 align="center">\n  Remarking\n</h1>\n\n<div align="center">\n  <a href="https://github.com/sabidib/remarking/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>\n  ·\n  <a href="https://github.com/sabidib/remarking/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>\n  .\n  <a href="https://github.com/sabidib/remarking/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>\n</div>\n\n<div align="center">\n<br />\n\n[![license](https://img.shields.io/github/license/sabidib/remarking.svg?style=flat-square)](LICENSE)\n[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/sabidib/remarking/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)\n[![code with hearth by sabidib](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-sabidib-ff1414.svg?style=flat-square)](https://github.com/sabidib)\n[![Documentation Status](https://readthedocs.org/projects/remarking/badge/?version=latest)](http://ansicolortags.readthedocs.io/?badge=latest)\n\n\n</div>\n\n\n## About\n\nRemarking is a command line tool for extracting highlights from documents on your reMarkable tablet.\n\nRemarking makes it as easy as possible to extract highlights from your annotated documents.\n\n\n![Remarking demo](docs/images/remarking_demo.gif)\n\n\n\nRemarking serves to be the first part of a highlight extraction pipeline.\n\nThis means, you can use Remarking to extract your highlights for then futher processing such as:\n  - Sending it to a service \n  - Combining it with another collection of highlights\n  - Further filtering of highlights with more tooling\n\nI found that there was no easy way of extracting highlights from the reMarkable. There were quite a few \ntools that focussed solely on extracting the highlights from the downloaded pdfs. However, nothing made\nthe process as easy as specifiying the folder to scan for documents.\n\n\n## Installation\n\n### Requirements\n\nYou will need at least:\n  - Python 3.7+\n  - Pip\n\n\n### Install\nTo get started you can install the package from pip with:\n```\npip3 install remarking\n```\n\nThe `remarking` command should then be available for you to use.\n\n\n## Usage\n\nCheck out the [docs](https://remarking.readthedocs.io/en/latest/) for help, or run `remarking --help`.\n\n\n### Token\n\nBefore you start you will need to grab a one-time authorization key from [https://my.remarkable.com/device/connect/desktop](https://my.remarkable.com/device/connect/desktop). This code is used to access the reMarkable cloud.\n\n[rmapy](https://github.com/subutux/rmapy) is used to access the reMarkable Cloud. After authorizing the first time, the tool will store an auth\ntoken in `~/.rmapi` for future use. You won\'t need to re-authorize by providing the token again until you deauthorize\nthe key.\n\nYou can specify the token through the `REMARKING_TOKEN` env var in addition to via command line with `--token`.\n\n### Modes\n\nThere are two main modes of usage of Remarking: run and persist.\n\n#### run\n\n`remarking run` will run the default extractors on all passed documents and folders. Highlights extracted\nare then output using the writer subcommand passed.\n\n```\nremarking run json books\n```\n\nThis command will run the default extractors on all documents in the books folder and output the highlights as json.\n\n#### persist\n\n`remarking persist` performs the same extraction on documents as run, however it maintains state\nof previously seen documents and highlights.\n\nBy default it creates a `remarking_database.sqlite3` database file in the current working directory that keeps track of\nseen highlights and documents.\n\nYou can also use your own database by providing the `--sqlalchemy` argument with a sqlalchemy connection string.\n\n```\nremarking persist json books\n```\n\nThis command will run the default extractors on all documents in the books folder and output the highlights as json.\n\nAll documents and their highlights found would also be added to the sqlite3 database `remarking_database.sqlite3`.\n\nA second run would return no new highlights if the documents in the books folder are not modified.\n\n## Examples\n\nYou can check out some examples in [the examples section of the docs](https://remarking.readthedocs.io/en/latest/examples.html).\n\n## Roadmap\n\nSee the [open issues](https://github.com/sabidib/remarking/issues) for a list of proposed features (and known issues).\n\n## Built With\n\n  - Python 3\n  - [rmapy](https://github.com/subutux/rmapy)\n  - [click](https://click.palletsprojects.com/en/8.0.x/)\n  - [sqlalchemy](https://www.sqlalchemy.org/)\n\n## Support\n\nReach out to the maintainer at one of the following places:\n\n\n- [GitHub issues](https://github.com/sabidib/remarking/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)\n- The email which is located [in this GitHub profile](https://github.com/sabidib)\n\n\n## Contributing\n\nFirst off, thanks for taking the time to contribute! Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly appreciated**.\n\nWe have set up a separate document containing our [contribution guidelines](CONTRIBUTING.md).\n\nThank you for being involved!\n\n## Authors & contributors\n\nThe original setup of this repository is by [Samy Abidib](https://github.com/sabidib).\n\nFor a full list of all authors and contributors, check [the contributor\'s page](https://github.com/sabidib/remarking/contributors).\n\n## Security\n\nRemarking follows good practices of security, but 100% security can\'t be granted in software.\nRemarking is provided **"as is"** without any **warranty**. Use at your own risk.\n\n_For more info, please refer to [security](SECURITY.md)._\n\n## License\n\nThis project is licensed under the **GPL v3** license.\n\nSee [LICENSE](LICENSE) for more information.\n\n## Acknowledgements\n\n* [rmapy](https://github.com/subutux/rmapy)\n* [remarks](https://github.com/lucasrla/remarks)\n* [biff](https://github.com/soulisalmed/biff)\n* [sqlalchemy](https://www.sqlalchemy.org/)\n* [The unofficial reMarkable discord](https://discord.gg/u3P9sDW)\n\n',
    'author': 'sabidib',
    'author_email': 'samy@sabidib.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://remarking.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
