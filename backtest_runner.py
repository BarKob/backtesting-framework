from portfolio import Backtester
from strategy import strategy, multi_asset_strategy
from data_import import data_loader
from metrics import Metrics
from visual import visualise
import pandas as pd

def run_the_backtester(tickers: str | list, start_date: str, end_date: str, benchmark: str | list, starting_capital: int, Strategy: strategy | multi_asset_strategy | list, Benchmark_Strategy: strategy = strategy(values = {}, signals = {"buy&hold": lambda row: True}), data_before_benchmark: int = 0):

    # Data processing, calculating signals based on quantitative data, preparing data for visualization, calculating metrics for startegy performance evaluation, visualization
    data_download_start_date = pd.to_datetime(start_date) - pd.Timedelta(days = data_before_benchmark) * 2
    
    Data = data_loader(tickers, data_download_start_date, end_date).load_data()

    Data_For_Backtesting = {}

    if isinstance(Strategy, list):
        for strat in Strategy:
            strat = strat.calculate_signal(Data)
            Data_For_Backtesting = Data_For_Backtesting | strat
    else:
        Data_For_Backtesting = Strategy.calculate_signal(Data)

    if data_before_benchmark > 0:
        Data_For_Backtesting = {asset_name: data_for_asset.loc[start_date:] for asset_name, data_for_asset in Data_For_Backtesting.items()}

    Benchmark_Data = data_loader(benchmark, start_date, end_date).load_data()
    Benchmark_Data = Benchmark_Strategy.calculate_signal(Benchmark_Data)
    Benchmark = Backtester(starting_capital)
    Benchmark_Final_data = Benchmark.backtest(Benchmark_Data)
    Benchmark_Final_metrics = Metrics(Benchmark_Final_data).calculate_metrics()

    Backtest = Backtester(starting_capital)
    Final_data = Backtest.backtest(Data_For_Backtesting)
    Final_metrics = Metrics(Final_data).calculate_metrics()

    visualise(Final_data, Benchmark_Final_data, Final_metrics, Benchmark_Final_metrics)