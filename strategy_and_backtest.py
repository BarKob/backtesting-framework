from portfolio import Backtester
from strategy import strategy, multi_asset_startegy
from data_import import data_loader
from metrics import Metrics

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
# for a typical buy & hold benchmark startegy: values = {}, signals = {"buy&hold": lambda row: True}

'''
EXAMPLE:

tickers = [
    "GLD",
    "AAPL",
    "TLT"
]

start_date = "2015-01-01"
end_date = "2025-01-01"
benchmark = "SPY"
starting_capital = 10000

Strategy = strategy(values = {
        "pct_change_20": lambda row: row["Close"].pct_change(20)
    }, signals = {
        "pct_change_20>0": lambda row: row["pct_change_20"] > 0
    })

Benchmark_Strategy = strategy(values = {
    }, signals = {
        "buy&hold": lambda row: True
    })
'''

# Data processing, calculating signals based on quantitative data, preparing data for visualization, calculating metrics for startegy performance evaluation
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