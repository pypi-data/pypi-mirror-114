# SIGMATMPY

> SIGMATMPY-library is an APIRequest driven trading and monitoring platform. Each functionality (trades, price etc.) is represented by it's own class covering all aspect of that functionality.


## Getting Started

### Installation

```sh
$ pip install sigmatmpy
```

### Basic functions

```sh
import sigmatmpy

# initualize APIRequest token
username = 'username'
password = 'password'
API = sigmatmpy.API(username,password)

# open_order(symbol, cmd, volume, price, slippage, stoploss, takeprofit,comment)
API.open_order('EURUSD', 1, 0.01, 1.18245, 3, 0, 0,'comment')

# close_order(ticket, volume, price)
API.close_order(9999999,0.01,1.18245)

# trades_history_by_datetime(start_time, end_time)
API.trades_history_by_datetime('2021-07-04 000000', '2021-07-16 075150')

# trades_history_by_unixtime(start_time_ctm, end_time_ctm)
API.trades_history_by_unixtime(1625991769, 1626423769)

# opened_trades()
API.opened_trades()

# account_info()
API.account_info()

# server_time()
API.server_time()
```

### Price data

```sh
# initialize data streaming for XAUUSD
API.initialize_price_stream('XAUUSD')

# get current price
API.current_price()

# get XAUUSD 5 min bar chart data
API.bar_chart('XAUUSD', 5)

# check appearance of new bar
API.check_new_bar('XAUUSD', 5)

```

## Release History 版本历史


## Authors 关于作者

* **SIGMATM** - *Initial work* - [SIGMATM]

查看更多关于这个项目的贡献者，请阅读 [contributors](#) 

## License 授权协议

这个项目 MIT 协议， 请点击 [LICENSE.md](LICENSE.md) 了解更多细节。