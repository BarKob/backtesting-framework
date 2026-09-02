from data_import import data_loader
from strategy import strategy
import pandas as pd

class backtester:

    def __init__(self, starting_capital, data):
        self.starting_capital = starting_capital
        self.data = data
        self.portfolio_history = pd.DataFrame(index = data.index, columns = ["cash", "shares_owned", "assets_value", "portfolio_value"], dtype = (int))

    def execute_strategy(self):
        self.portfolio_history.index.name = "Date"
        print(self.data.head())
        current_capital = self.starting_capital
        shares_owned = 0
        print(self.portfolio_history.dtypes)
        self.portfolio_history.loc[self.data.index[0]] =  {
    "cash": current_capital,
    "shares_owned": 0,
    "assets_value": 0,
    "portfolio_value": current_capital
}
        for date, row in self.data.iterrows():
            print(self.portfolio_history.loc[date, "cash"])
            if self.data.loc[date, "signal"] == True and self.portfolio_history.loc[date, "cash"] > 0:
                trade_value = self.portfolio_history.loc[date, "cash"]
                shares_to_buy = trade_value / self.data.loc[date, "Close"]
                current_capital -= trade_value
                shares_owned += shares_to_buy
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "cash"] = current_capital
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "shares_owned"] = shares_owned
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "assets_value"] = shares_owned * self.data.loc[date, "Close"]
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "portfolio_value"] = current_capital + shares_owned * self.data.loc[date, "Close"]
            elif self.data.loc[date, "signal"] == False and self.portfolio_history.loc[date, "shares_owned"] > 0:
                trade_value = self.portfolio_history.loc[date, "shares_owned"] * self.data.loc[date, "Close"]
                current_capital += trade_value
                shares_owned = 0
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "cash"] = current_capital
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "shares_owned"] = shares_owned
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "assets_value"] = shares_owned * self.data.loc[date, "Close"]
                self.portfolio_history.loc[date + pd.Timedelta(days=1), "portfolio_value"] = current_capital + shares_owned * self.data.loc[date, "Close"]
        return self.portfolio_history
    def update_portfolio_history(self, current_capital, shares_owned):
        self.portfolio_history["cash"] = current_capital
        self.portfolio_history["shares_owned"] = shares_owned
        self.portfolio_history["assets_value"] = shares_owned * self.data["Close"]
        self.portfolio_history["portfolio_value"] = self.portfolio_history["cash"] + self.portfolio_history["assets_value"]
        return self.portfolio_history

Data = data_loader("MSFT", "2020-01-01", "2020-02-01").load_data()
Strategy = strategy(values = {"o-c": lambda row: row["Open"] - row["Close"]}, signals = {"o-c>0": lambda row: row["o-c"] > 0})
Data = Strategy.calculate_signal(Data)
Backtest = backtester(10000, Data)
print(Backtest.execute_strategy())