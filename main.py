from strategy import strategy, multi_asset_strategy
from backtest_runner import run_the_backtester
import pandas as pd

#Strategy & Backtest declaration

tickers = [] # str for singular asset, list of strings for multiple assets
start_date = "" # "YYYY-MM-DD"
end_date = "" # "YYYY-MM-DD"
benchmark = [] # str for singular asset, list of strings for multiple assets
starting_capital = int # starting capital
lookback_days = int #how far should the backtester go in order to account for rolling statistics

Strategy = strategy() 
# creation of a strategy object with arguments: 
# values: dict ("value_name": lambda function to calculate value for each row of market data)
# signals: dict ("signal_name": lambda function to calculate boolean value for each row of market data)
# also possible to create a multi-asset startegy (class multi_asset_startegy), for which the signal may be calculated based on another assets data
# additional argument:
# assets_to_trade: str | list (assets which we want to trade based on the calculated signal)

Benchmark_Strategy = strategy() 
# same as above
# defaults to a typical SPY buy & hold benchmark startegy: values = {}, signals = {"buy&hold": lambda row: True}

run_the_backtester(tickers, start_date, end_date, benchmark, starting_capital, Strategy, Benchmark_Strategy, lookback_days)