from strategy import multi_asset_strategy
from backtest_runner import run_the_backtester

tickers = ["MSFT", "AAPL"]
start_date = "2015-01-01"
end_date = "2017-01-01"
benchmark = "SPY"
starting_capital = 10000

Strategy1 = multi_asset_strategy("MSFT", values = {
        "AAPL_pct_change_60": lambda data: data["AAPL"]["Close"].pct_change(60),
        "MSFT_pct_change_60": lambda data: data["MSFT"]["Close"].pct_change(60)
    }, signals = {
        "MSFT<AAPL_pctc60": lambda row: row["MSFT_pct_change_60"] < row["AAPL_pct_change_60"]
    })

Strategy2 = multi_asset_strategy("AAPL", values = {
        "AAPL_pct_change_60": lambda data: data["AAPL"]["Close"].pct_change(60),
        "MSFT_pct_change_60": lambda data: data["MSFT"]["Close"].pct_change(60)
    }, signals = {
        "AAPL<MSFT_pctc60": lambda row: row["AAPL_pct_change_60"] < row["MSFT_pct_change_60"]
    })

Strategy = [Strategy1, Strategy2]

run_the_backtester(tickers, start_date, end_date, benchmark, starting_capital, Strategy, lookback_days = 60)
