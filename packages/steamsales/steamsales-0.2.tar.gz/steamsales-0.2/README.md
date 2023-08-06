# Steam Sales

Python API Wrapper for [PrepareYourWallet](https://prepareyourwallet.com/) service. 

## What is PrepareYourWallet?

See when the next Steam Sale will start and how long remains with our countdown timer. PrepareYourWallet.com is tracking all type of sales on the Steam Store such as holiday, lunar new year, summer, halloween and fall sale.

Valve don’t tend to announce their sales in advance. However, by looking at the previous years we can approximately predict when the next one will be. Sometimes, dates can also leak from multiple sources like PayPal.

## Requirements

[requests](https://pypi.org/project/requests/) - required.

[lxml](https://pypi.org/project/lxml/) - required.

[bs4](https://pypi.org/project/bs4/) - required.

## Installation
```bash
pip3 install steamsales
```
## Usage
```python
from steamsales import info as s

print(
    f'Sale Name: {s.sale_name}' +
    f'Start Date: {s.start_date}' +
    f'End Date: {s.end_date}' +
    f'Countdown: {s.countdown}' +
    f'Status: {s.status}'
)
```
