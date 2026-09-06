from strategy import strategy
from backtest_runner import run_the_backtester
import pandas as pd

tickers = "SPY"

start_date = "2015-01-01"
end_date = "2025-01-01"
benchmark = "SPY"
starting_capital = 10000

Strategy = strategy(values = {
        "sma_200": lambda row: row["Close"].rolling(200).mean(),
        "sma_50": lambda row: row["Close"].rolling(50).mean()
    }, signals = {
        "sma_200 < sma_50": lambda row: row["sma_200"] < row["sma_50"]
    })

run_the_backtester(tickers, start_date, end_date, benchmark, starting_capital, Strategy)
