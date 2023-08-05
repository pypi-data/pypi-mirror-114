# Easy Equities and Satrix Python Client

Unofficial Python client for [Easy Equities](easyequities.io/) and [Satrix](satrix.co.za/). Intended for personal use.


## Installation

```
pip install easy-equities-client
```

## Usage

```python
from easy_equities_client.clients import EasyEquitiesClient # or SatrixClient

client = EasyEquitiesClient()
client.login(username='your username', password='your password')

# List accounts
accounts = client.accounts.list()
"""
[
    Account(id='12345', name='EasyEquities ZAR', trading_currency_id='2'),
    Account(id='12346', name='TFSA', trading_currency_id='3'),
    ...
]
"""

# Get account holdings
holdings = client.accounts.holdings(accounts[0].id)
"""
[
    {
        "name": "CoreShares Global DivTrax ETF",
        "contract_code": "EQU.ZA.GLODIV",
        "purchase_value": "R2 000.00",
        "current_value": "R3 000.00",
        "current_price": "R15.50",
        "img": "https://resources.easyequities.co.za/logos/EQU.ZA.GLODIV.png",
        "view_url": "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000254249",
        "isin": "ZAE000254249"
    },
    ...
]
"""

# Get account valuations
valuations = client.accounts.valuations(accounts[0].id)
"""
{
    "NetInterestOnCashItems": [
        {
            "Label": "Total Interest on Free Cash",
            "Value": "R10.55"
        },
        ...
    ],
    "AccrualSummaryItems": [
        {
            "Label": "Net Accrual",
            "Value": "R2.00"
        },
        ...
    ],
    "TopSummary": {
        "AccountValue": 300000.50,
        "AccountCurrency": "ZAR",
        "AccountNumber": "EE123456-111111",
        "AccountName": "EasyEquities ZAR",
        "PeriodMovements": [
            {
                "ValueMoveLabel": "Profit & Loss Value",
                "ValueMove": "R5 000.00",
                "PercentageMoveLabel": "Profit & Loss",
                "PercentageMove": "15.00%",
                "PeriodMoveHeader": "Movement on Current Holdings:"
            }
        ]
    },
    "InvestmentTypesAndManagers": {
        "InvestmentTypes": [
            {
                "Key": "ETFs",
                "Value": "R25 000.90",
                "Percentage": 85.00
            },
            ...
        ]
    },
    "InvestmentSummaryItems": [
        {
            "Label": "Total Profit / Loss on Current Holdings",
            "Value": "R4 000.50 / 15.00%",
            "IsPositive": true
        },
        ...
    ]
    "CostsSummaryItems": [
        {
            "Label": "Total Brokerage and Statutory Costs",
            "Value": "R300.00"
        },
        ...
    ]
    ...
}
"""

# Get account transactions
transactions = client.accounts.transactions(accounts[0].id)
"""
[
    {
        "TransactionId": 0,
        "DebitCredit": 200.00,
        "Comment": "Account Balance Carried Forward",
        "TransactionDate": "2020-07-21T01:00:00",
        "LogId": 123456789,
        "ActionId": 0,
        "Action": "Account Balance Carried Forward",
        "ContractCode": ""
    },
        {
        "TransactionId": 0,
        "DebitCredit": 50.00,
        "Comment": "CoreShares Global DivTrax ETF-Foreign Dividends @15.00",
        "TransactionDate": "2020-11-19T14:30:00",
        "LogId": 123456790,
        "ActionId": 122,
        "Action": "Foreign Dividend",
        "ContractCode": "EQU.ZA.GLODIV"
    },
    ...
]
```

## Contributing

See [Contributing](./CONTRIBUTING.md)