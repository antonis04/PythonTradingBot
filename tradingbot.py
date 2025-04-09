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
        "quantity": 10,
        "side": "buy"
    }

    def initialize(self, symbol=""):
        self.sleeptime = "10M"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        side = self.parameters["side"]
        order = self.create_order(symbol, quantity, side)
        self.submit_order(order)
        self.sell_if_needed(symbol)

    def sell_if_needed(self, symbol):
        """
        Sprawdza warunki sprzedaży i sprzedaje, jeśli to konieczne.
        """
        # Przykładowy warunek sprzedaży: cena zamknięcia spadła poniżej określonego progu
        current_price = self.get_last_price(symbol)
        sell_threshold = 400  # Próg sprzedaży (przykładowa wartość)

        if current_price < sell_threshold:
            sell_order = self.create_order(symbol, self.parameters["quantity"], "sell")
            self.submit_order(sell_order)

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
