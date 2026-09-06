from strategy import strategy, multi_asset_startegy
from backtest_runner import run_the_backtester
import pandas as pd

#Strategy & Backtest declaration

tickers = [] # str for singular asset, list of strings for multiple assets
start_date = "" # "YYYY-MM-DD"
end_date = "" # "YYYY-MM-DD"
benchmark = [] # str for singular asset, list of strings for multiple assets
starting_capital = int # starting capital

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

'''
#EXAMPLE:

tickers = ["MSFT", "AAPL"]

start_date = "2015-01-01"
end_date = "2025-01-01"
benchmark = "SPY"
starting_capital = 10000

Strategy = strategy(values = {
        "sma_20": lambda row: row["Close"].rolling(20).mean(),
        "sma_60": lambda row: row["Close"].rolling(60).mean()
    }, signals = {
        "sma_20 > sma_60": lambda row: row["sma_20"] > row["sma_60"]
    })

Benchmark_Strategy = strategy(values = {
    }, signals = {
        "buy&hold": lambda row: True
    })
'''
'''
# Data processing, calculating signals based on quantitative data, preparing data for visualization, calculating metrics for startegy performance evaluation, visualization
Benchmark_Data = data_loader(benchmark, start_date, end_date).load_data()
Benchmark_Data = Benchmark_Strategy.calculate_signal(Benchmark_Data)
Benchmark = Backtester(starting_capital)
Benchmark_Final_data = Benchmark.backtest(Benchmark_Data)
Benchmark_Final_metrics = Metrics(Benchmark_Final_data).calculate_metrics()

Data = data_loader(tickers, start_date, end_date).load_data()
Data = Strategy.calculate_signal(Data)
Backtest = Backtester(starting_capital)
Final_data = Backtest.backtest(Data)
Final_metrics = Metrics(Final_data).calculate_metrics()

visualise(Final_data, Benchmark_Final_data, Final_metrics, Benchmark_Final_metrics)

tickers = ["MSFT", "AAPL"]
start_date = "2015-01-01"
end_date = "2025-01-01"
benchmark = "SPY"
starting_capital = 10000

Strategy1 = multi_asset_startegy("MSFT", values = {
        "AAPL_pct_change_60": lambda data: data["AAPL"]["Close"].pct_change(20),
        "MSFT_pct_change_60": lambda data: data["MSFT"]["Close"].pct_change(20)
    }, signals = {
        "MSFT<AAPL_pctc60": lambda row: row["MSFT_pct_change_60"] < row["AAPL_pct_change_60"]
    })

Strategy2 = multi_asset_startegy("AAPL", values = {
        "AAPL_pct_change_60": lambda data: data["AAPL"]["Close"].pct_change(20),
        "MSFT_pct_change_60": lambda data: data["MSFT"]["Close"].pct_change(20)
    }, signals = {
        "AAPL<MSFT_pctc60": lambda row: row["AAPL_pct_change_60"] < row["MSFT_pct_change_60"]
    })

Strategy = [Strategy1, Strategy2]

Benchmark_Strategy = strategy(values = {
    }, signals = {
        "buy&hold": lambda row: True
    })
'''
run_the_backtester(tickers, start_date, end_date, benchmark, starting_capital, Strategy, Benchmark_Strategy)