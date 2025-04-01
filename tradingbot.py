from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader

ALPACA_CONFIG = {
    "API_KEY": "PK8QOO4X5ATY2WLGTBR0",
    "API_SECRET": "CZstoEfdcAV6fc2pwCJKdh20dOwxsxdm6bMz8ba1",
    # Set this to False to use a live account
    "PAPER": True
}

class MyStrategy(Strategy):
    parameters = {
        "symbol": "SPY",
        "quantity": 1,
        "side": "buy"

    }

    def initialize(self, symbol=""):
        self.sleeptime = "180M"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        side = self.parameters["side"]
        order = self.create_order(symbol, quantity, side)
        self.submit_order(order)

trader = Trader()
broker = Alpaca(ALPACA_CONFIG)
strategy = MyStrategy(broker=broker, parameters={"symbol": "SPY"})

backtesting_start = datetime(2024, 1, 1)
backtesting_end = datetime(2024, 12, 31)
strategy.run_backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    parameters={"symbol": "SPY"}
)



trader.add_strategy(strategy)
trader.run_all()