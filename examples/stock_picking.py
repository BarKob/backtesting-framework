from strategy import strategy
from backtest_runner import run_the_backtester

tickers = ["MSFT", "GOOG", "AAPL"]

start_date = "2007-01-01"
end_date = "2017-01-01"
benchmark = "SPY"
starting_capital = 10000

Strategy = strategy(values = {}, signals = {
        "buy&hold": lambda row: True
    })

run_the_backtester(tickers, start_date, end_date, benchmark, starting_capital, Strategy)