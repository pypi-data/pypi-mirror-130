# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypipet',
 'pypipet.cli',
 'pypipet.core',
 'pypipet.core.fileIO',
 'pypipet.core.logging',
 'pypipet.core.model',
 'pypipet.core.operations',
 'pypipet.core.pipeline',
 'pypipet.core.shop_conn',
 'pypipet.core.sql',
 'pypipet.core.transform',
 'pypipet.plugins',
 'pypipet.plugins.canadapost',
 'pypipet.plugins.gg_merchant.shopping',
 'pypipet.plugins.gg_merchant.shopping.content',
 'pypipet.plugins.paypal',
 'pypipet.plugins.woocommerce']

package_data = \
{'': ['*'], 'pypipet.core': ['default_setting/*']}

install_requires = \
['click>=7.0,<8.0',
 'pandas>=1.2.0,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.4.27,<2.0.0']

entry_points = \
{'console_scripts': ['pypipet = pypipet.cli:cli']}

setup_kwargs = {
    'name': 'pypipet',
    'version': '0.0.11a0',
    'description': 'pypipet',
    'long_description': '[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/pip/)\n[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)\n[![Generic badge](https://img.shields.io/badge/Status-dev-orange.svg)](https://shields.io/)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![Generic badge](https://img.shields.io/badge/Pypi package-0.0.1a-blue.svg)](https://shields.io/)\n[![Generic badge](https://img.shields.io/badge/Python-3.8-blue.svg)](https://shields.io/)\n\n#### intro\n\nPipet is an open source project, aiming to integrate data flows in online retailing. It simplifies the data pipeline of ecommerce, for example, adding catalog, update product, manage inventory and orders, etc. It is customized for small business who are selling on wordpress (for example, with woocommerce), shopify, ebay, amazon, Paypal, etc. It extremely handy if the business is selling on multiple platforms. Pipet is under dev. The latest version 0.0.1a. \n\n* For source code,  visit  [github repositoty](https://).\n* For documentation, vist [docs]()\n\n### installation\n\n    pip install pypipet\n\n    or \n\n    pip3 install pypipet\n\n#### to-do list\n\n- [ ] connect to shopify\n- [ ] connect to bigcommerce\n- [ ] add email template\n- [ ] UI\n- [ ] connect to Google Analytics',
    'author': 'pypipet and contributors',
    'author_email': 'pypipet@gmail.com',
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
