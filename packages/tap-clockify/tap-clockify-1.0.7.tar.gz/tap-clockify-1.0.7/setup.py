# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_clockify', 'tap_clockify.schemas', 'tap_clockify.tests']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.7-beta.0,<22.0', 'requests>=2.25.1,<3.0.0', 'singer-sdk']

entry_points = \
{'console_scripts': ['tap-clockify = tap_clockify.tap:TapClockify.cli']}

setup_kwargs = {
    'name': 'tap-clockify',
    'version': '1.0.7',
    'description': 'Singer tap for Clockify, built with the Meltano SDK for Singer Taps.',
    'long_description': '# tap-clockify\n\n![Test Packages](https://github.com/immuta/tap-clockify/actions/workflows/test_package.yml/badge.svg)\n![Last Release Published](https://github.com/immuta/tap-clockify/actions/workflows/publish_package.yml/badge.svg)\n\n**Author**: Stephen Bailey (sbailey@immuta.com)\n\nThis is a [Singer](http://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).\n\nIt can generate a catalog of available data in Clockify and extract the following resources:\n\n- clients\n- projects\n- tags\n- tasks\n- time entries\n- users\n- workspaces\n\n### Configuration\n\n```\n{\n  "api_key": "string",\n  "workspace": "string",\n  "start_date": "2020-04-01T00:00:00Z"\n}\n```\n\n### Quick Start\n\n1. Install\n\n```bash\ngit clone git@github.com:immuta/tap-clockify.git\ncd tap-clockify\npip install .\n```\n\n2. Get an [API key](https://clockify.me/developers-api) from Clockify\n\n3. Create the config file.\n\nThere is a template you can use at `config.json.example`, just copy it to `config.json` in the repo root and insert your token\n\n4. Run the application to generate a catalog.\n\n```bash\ntap-clockify -c config.json --discover > catalog.json\n```\n\n5. Select the tables you\'d like to replicate\n\nStep 4 generates a a file called `catalog.json` that specifies all the available endpoints and fields. You\'ll need to open the file and select the ones you\'d like to replicate. See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format) for more information on how tables are selected.\n\n6. Run it!\n\n```bash\ntap-clockify -c config.json --catalog catalog.json\n```\n\n### Acknowledgements\n\nWould like to acknowledge the folks at Fishtown Analytics whose [`tap-framework`](https://github.com/fishtown-analytics/tap-framework) and [`tap-lever`](https://github.com/fishtown-analytics/tap-lever) packages formed the foundation for this package.\n\nCopyright &copy; 2019 Immuta\n',
    'author': 'Stephen Bailey',
    'author_email': 'stkbailey@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/immuta/tap-clockify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
