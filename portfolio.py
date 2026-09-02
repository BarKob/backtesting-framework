from data_import import data_loader
from strategy import strategy
import pandas as pd

class Backtester:

    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.assets_data = {}
        self.portfolio_history = {}
        self.daily_data = []

    def buy_sell_decision(self, asset: str, signal: bool, price: float):
        if signal and self.assets_data[asset]["cash"] > 0:
            trade_value = self.assets_data[asset]["cash"]
            shares_to_buy = trade_value / price
            self.assets_data[asset]["cash"] -= trade_value
            self.assets_data[asset]["shares_owned"] += shares_to_buy
        elif signal == False and self.assets_data[asset]["shares_owned"] > 0:
            trade_value = self.assets_data[asset]["shares_owned"] * price
            self.assets_data[asset]["cash"] += trade_value
            self.assets_data[asset]["shares_owned"] = 0

    def portfolio_update(self, asset: str, price: float):
        self.assets_data[asset]["shares_value"] = self.assets_data[asset]["shares_owned"] * price
        self.assets_data[asset]["total_value"] = self.assets_data[asset]["cash"] + self.assets_data[asset]["shares_value"]
        self.portfolio_history[asset].append(self.assets_data[asset]["total_value"])

    def backtest(self, data: pd.DataFrame | dict[str, pd.DataFrame]):
        if isinstance(data, pd.DataFrame):
            data = {"Asset": data}
        for asset, small_data in data.items():
            self.assets_data[asset] = {"cash": self.initial_capital / len(data), "shares_owned": 0, "shares_value": 0, "total_value": 0,}
            self.portfolio_history[asset] = []
            for index, row in small_data.iterrows():
                self.buy_sell_decision(asset, row["signal"], row["Close"])
                self.portfolio_update(asset, row["Close"])
        self.portfolio_history["Total_Portfolio_Value"] = pd.Series([sum(values) for values in zip(*self.portfolio_history.values())], index = next(iter(data.values())).index)
        return self.portfolio_history 
