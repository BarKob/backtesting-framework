from portfolio import Backtester
from strategy import strategy, multi_asset_startegy
from data_import import data_loader
from metrics import Metrics
import matplotlib.pyplot as plt

#Strategy declaration
tickers = [
    "GLD",
    "AAPL",
    "TLT"
]

start_date = "2015-01-01"
end_date = "2025-01-01"
benchmark = "SPY"
starting_capital = 10000

Data = data_loader(tickers, start_date, end_date).load_data()

Benchmark_Data = data_loader(benchmark, start_date, end_date).load_data()

'''
Strategy = strategy(values = {
        "pct_change_20": lambda row: row["Close"].pct_change(20)
    }, signals = {
        "pct_change_20>0": lambda row: row["pct_change_20"] > 0
    })
'''

Strategy_1 =  multi_asset_startegy(["GLD"],
                                    values = {"pct_change_20": lambda row: row["Close"].pct_change(20)}, 
                                    signals = {">TLTpctchange": lambda data: data["GLD"]["pct_change_20"] > data["TLT"]["pct_change_20"],
                                               ">AAPLpctchange": lambda data: data["GLD"]["pct_change_20"] > data["AAPL"]["pct_change_20"]}).calculate_signal(Data)

Strategy_2 =  multi_asset_startegy(["AAPL"],
                                    values = {"pct_change_20": lambda row: row["Close"].pct_change(20)}, 
                                    signals = {">GLDpctchange": lambda data: data["AAPL"]["pct_change_20"] > data["GLD"]["pct_change_20"],
                                               ">TLTpctchange": lambda data: data["AAPL"]["pct_change_20"] > data["TLT"]["pct_change_20"]}).calculate_signal(Data)

Strategy_3 =  multi_asset_startegy(["TLT"],
                                    values = {"pct_change_20": lambda row: row["Close"].pct_change(20)}, 
                                    signals = {">GLDpctchange": lambda data: data["TLT"]["pct_change_20"] > data["GLD"]["pct_change_20"],
                                               ">AAPLpctchange": lambda data: data["TLT"]["pct_change_20"] > data["AAPL"]["pct_change_20"]}).calculate_signal(Data)

Data = Strategy_1 | Strategy_2 | Strategy_3

Benchmark_Strategy = strategy(values = {
    }, signals = {
        "buy&hold": lambda row: True
    })

Benchmark_Data = Benchmark_Strategy.calculate_signal(Benchmark_Data)
Benchmark = Backtester(starting_capital)
Benchmark_Final_data = Benchmark.backtest(Benchmark_Data)
Benchmark_Final_metrics = Metrics(Benchmark_Final_data).calculate_metrics()
'''
Data = Strategy.calculate_signal(Data)
'''
Backtest = Backtester(starting_capital)
Final_data = Backtest.backtest(Data)
Final_metrics = Metrics(Final_data).calculate_metrics()

#Visualization
fig, axes = plt.subplots(3, 1)

axes[0].set_title("Portfolio against Benchmark")
axes[1].set_title("Portfolio components")

for asset, data in list(Final_data.items())[:-1]:
    axes[1].plot(data, label = asset)

for benchmark_asset, data in list(Benchmark_Final_data.items())[:-1]:
    axes[0].plot(data, label = "Benchmark", lw = 4)

axes[0].plot(Final_data["Total_Portfolio_Value"].tolist(), label = "Portfolio Value")

axes[0].legend()
axes[1].legend()


metrics_text = "STRATEGY: \n" + "\n".join(f"{metric_name}:  {round(value, 2)}" for metric_name, value in Final_metrics.items())
benchmark_metrics_text = "BENCHMARK: \n" + "\n".join(f"{metric_name}:  {round(value, 2)}" for metric_name, value in Benchmark_Final_metrics.items())

axes[2].axis("off")
axes[2].text(0.35, 0.5, metrics_text, transform = axes[2].transAxes, verticalalignment = "center")
axes[2].text(0.65, 0.5, benchmark_metrics_text, transform = axes[2].transAxes, verticalalignment = "center")

plt.tight_layout()
plt.show()
