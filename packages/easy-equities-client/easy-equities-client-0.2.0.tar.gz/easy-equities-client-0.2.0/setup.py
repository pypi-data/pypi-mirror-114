# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_equities_client',
 'easy_equities_client.accounts',
 'easy_equities_client.instruments',
 'easy_equities_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'easy-equities-client',
    'version': '0.2.0',
    'description': 'Unofficial Easy Equities and Satrix Python Client',
    'long_description': '# Easy Equities and Satrix Python Client\n\nUnofficial Python client for [Easy Equities](easyequities.io/) and [Satrix](satrix.co.za/). Intended for personal use.\n\n\n## Installation\n\n```\npip install easy-equities-client\n```\n\n## Usage\n\n```python\nfrom easy_equities_client.clients import EasyEquitiesClient # or SatrixClient\n\nclient = EasyEquitiesClient()\nclient.login(username=\'your username\', password=\'your password\')\n\n# List accounts\naccounts = client.accounts.list()\n"""\n[\n    Account(id=\'12345\', name=\'EasyEquities ZAR\', trading_currency_id=\'2\'),\n    Account(id=\'12346\', name=\'TFSA\', trading_currency_id=\'3\'),\n    ...\n]\n"""\n\n# Get account holdings\nholdings = client.accounts.holdings(accounts[0].id)\n"""\n[\n    {\n        "name": "CoreShares Global DivTrax ETF",\n        "contract_code": "EQU.ZA.GLODIV",\n        "purchase_value": "R2 000.00",\n        "current_value": "R3 000.00",\n        "current_price": "R15.50",\n        "img": "https://resources.easyequities.co.za/logos/EQU.ZA.GLODIV.png",\n        "view_url": "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000254249",\n        "isin": "ZAE000254249"\n    },\n    ...\n]\n"""\n\n# Get account valuations\nvaluations = client.accounts.valuations(accounts[0].id)\n"""\n{\n    "TopSummary": {\n        "AccountValue": 300000.50,\n        "AccountCurrency": "ZAR",\n        "AccountNumber": "EE123456-111111",\n        "AccountName": "EasyEquities ZAR",\n        "PeriodMovements": [\n            {\n                "ValueMoveLabel": "Profit & Loss Value",\n                "ValueMove": "R5 000.00",\n                "PercentageMoveLabel": "Profit & Loss",\n                "PercentageMove": "15.00%",\n                "PeriodMoveHeader": "Movement on Current Holdings:"\n            }\n        ]\n    },\n    "NetInterestOnCashItems": [\n        {\n            "Label": "Total Interest on Free Cash",\n            "Value": "R10.55"\n        },\n        ...\n    ],\n    "AccrualSummaryItems": [\n        {\n            "Label": "Net Accrual",\n            "Value": "R2.00"\n        },\n        ...\n    ],\n    ...\n}\n"""\n\n# Get account transactions\ntransactions = client.accounts.transactions(accounts[0].id)\n"""\n[\n    {\n        "TransactionId": 0,\n        "DebitCredit": 200.00,\n        "Comment": "Account Balance Carried Forward",\n        "TransactionDate": "2020-07-21T01:00:00",\n        "LogId": 123456789,\n        "ActionId": 0,\n        "Action": "Account Balance Carried Forward",\n        "ContractCode": ""\n    },\n        {\n        "TransactionId": 0,\n        "DebitCredit": 50.00,\n        "Comment": "CoreShares Global DivTrax ETF-Foreign Dividends @15.00",\n        "TransactionDate": "2020-11-19T14:30:00",\n        "LogId": 123456790,\n        "ActionId": 122,\n        "Action": "Foreign Dividend",\n        "ContractCode": "EQU.ZA.GLODIV"\n    },\n    ...\n]\n"""\n\n# Get historical data for an equity/instrument\nfrom easy_equities_client.instruments.types import Period\nhistorical_prices = client.instruments.historical_prices(\'EQU.ZA.SYGJP\', Period.ONE_MONTH)\n"""\n{\n    "chartData": {\n        "Dataset": [\n            41.97,\n            42.37,\n            ...\n        ],\n        "Labels": [\n            "25 Jun 21",\n            "28 Jun 21",\n            ...\n        ],\n        "TradingCurrencySymbol": "R",\n        ...\n    }\n}\n"""\n```\n\n## Example Use Cases\n\n### Show holdings total profits/losses\n\nRun a script to show your holdings and their total profits/losses, e.g. [show_holdings_profit_loss.py](./examples/show_holdings_profit_loss.py).\n\n![show_holdings_profit_loss.py example output](./examples/show_holdings_profit_loss_example.png)\n\n\n\n## Contributing\n\nSee [Contributing](./CONTRIBUTING.md)',
    'author': 'Delena Malan',
    'author_email': 'delena.malan@gmail.com',
    'maintainer': 'Delena Malan',
    'maintainer_email': 'delena.malan@gmail.com',
    'url': 'https://github.com/delenamalan/easy-equities-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
