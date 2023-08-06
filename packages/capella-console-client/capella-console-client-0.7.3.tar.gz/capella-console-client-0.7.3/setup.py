# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['capella_console_client']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'retrying>=1.3.3,<2.0.0',
 'rich>=10.5.0,<11.0.0']

extras_require = \
{'docs': ['Sphinx>=3.3,<4.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'sphinx-autobuild>=2020.9.1,<2021.0.0',
          'sphinx-copybutton>=0.3.1,<0.4.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0']}

setup_kwargs = {
    'name': 'capella-console-client',
    'version': '0.7.3',
    'description': 'Python SDK for api.capellaspace.com (search, order, download)',
    'long_description': '# 🛰️ capella-console-client 🐐\n\n[![Version](https://img.shields.io/pypi/v/capella-console-client.svg)](https://pypi.org/project/capella-console-client/)\n[![License](https://img.shields.io/pypi/l/capella-console-client.svg)](#)\n[![CI](https://github.com/capellaspace/console-client/workflows/CI/badge.svg)](#)\n[![Coverage](https://coveralls.io/repos/github/capellaspace/console-client/badge.svg?branch=main)](https://coveralls.io/github/capellaspace/console-client)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/capella-console-client.svg)](https://pypi.org/project/capella-console-client/)\n[![Documentation](https://readthedocs.org/projects/capella-console-client/badge/?version=main)](https://capella-console-client.readthedocs.io)\n\nPython SDK for api.capellaspace.com (search, order, download)\n\n\n## Installation\n\n```bash\npip install capella-console-client\n```\n\n## Requirements\n\n* python >= 3.6\n* `capella-console-client` requires an active account on [console.capellaspace.com](https://console.capellaspace.com/). Sign up for an account[here]](https://console.capellaspace.com/user/register/)\n\n\n## Usage\n\n![Quickstart](docs/images/quickstart.gif)\n\n```python\nfrom capella_console_client import CapellaConsoleClient\n\n# you will be prompted for console user (user@email.com)/ password before authenticating\nclient = CapellaConsoleClient(\n    verbose=True\n)\n\n# search for 2 open-data products\nstac_items = client.search(\n    instrument_mode="spotlight",\n    product_type__in=["SLC", "GEO"],\n    collections=["capella-open-data"],\n    limit=2\n)\n\n# order\norder_id = client.submit_order(items=stac_items, omit_search=True)\n\n# download\nproduct_paths = client.download_products(\n    order_id=order_id, \n    local_dir=\'/tmp\',\n    show_progress=True\n)\n```\n\n\n## Documentation\n\nThe documentation for `capella_console_client` can be found [here](https://capella-console-client.readthedocs.io).\n\n## Support\n\nPlease [open an issue](https://github.com/capellaspace/console-client/issues/new)\nwith enough information for us to reproduce your problem.\nA [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example)\nwould be very helpful.\n\n## Contributing\n\nContributions are very much welcomed and appreciated. See [how to contribute](https://capella-console-client.readthedocs.io/en/main/pages/contributors.html) for more information.\n\n\n## License\n• Licensed under the [MIT License](https://github.com/capellaspace/console-client/blob/master/LICENSE) • Copyright 2021 • Capella Space •\n',
    'author': 'Thomas Beyer',
    'author_email': 'thomas.beyer@capellaspace.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/capellaspace/console-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
