# Backtesting Framework

<u>A Python framework for backtesting signal-based systematic trading strategies with support for single- and multi-asset execution.</u>

The framework was built from scratch to provide a modular environment for testing systematic trading strategies on historical market data. It separates data acquisition, strategy declaration, signal generation, portfolio execution, performance evaluation, and visualization into independent components.

---

## Overview

The framework takes historical market data, applies a user-defined trading strategy, simulates portfolio execution, and evaluates the resulting performance against a benchmark.

The main workflow is:

```text
Strategy creation
        ↓
Historical Market Data
        ↓
    Data Loader
        ↓
 Signal Generation
        ↓
     Backtester
        ↓
 Portfolio History
        ↓
 Performance Metrics
        ↓
 Visualization & Benchmark Comparison
```

<u>The framework is designed in a modular way so that the framework is not tied to any strategy, the trading logic is separated from the portfolio execution and performance evaluation layers. This allows different strategies to be tested without modifying the underlying backtesting engine.</u>

---

## Features

### Strategy Definition

Strategies are defined through user-provided functions for calculating derived values and generating trading signals.

```python
Strategy = strategy(
    values={
        "sma_20": lambda row: row["Close"].rolling(20).mean(),
        "sma_60": lambda row: row["Close"].rolling(60).mean()
    },
    signals={
        "sma_20 > sma_60": lambda row: row["sma_20"] > row["sma_60"]
    }
)
```

<u>Strategy logic is decoupled from the backtesting engine through a flexible function-based interface.</u>

Multiple conditions can be combined into a final trading signal.

### Single-Asset Backtesting

The framework supports conventional single-asset systematic strategies where trading decisions are based on the quantitative data of one asset.

### Multi-Asset Backtesting

<u>The framework also supports multi-asset execution, allowing signals to be calculated using information from multiple assets and specifying which assets should actually be traded.</u>

This allows strategies to incorporate cross-asset information rather than restricting signals to the asset being traded.

For example, a strategy can use information from one asset to determine whether another asset should be traded.

### Portfolio Simulation

The `Backtester` class simulates portfolio execution by maintaining:

* Cash
* Shares owned
* Asset value
* Total portfolio value

<u>For multi-asset portfolios, the framework allocates the initial capital across the selected assets and aggregates their individual daily portfolio values into a total portfolio value series.</u>

### Benchmark Comparison

<u>Strategy performance can be evaluated against a separately constructed benchmark strategy.</u>

The framework supports constructing a simple buy-and-hold benchmark using the same strategy interface.

This makes it possible to compare both portfolio value and performance metrics rather than evaluating a strategy in isolation.

### Performance Metrics

The framework currently calculates:

* Total return
* Annualized volatility
* Maximum drawdown
* Annualized Sharpe ratio

<u>The Sharpe ratio incorporates a time-varying risk-free rate based on 3-month U.S. Treasury yields rather than assuming a constant zero risk-free rate.</u>

The risk-free-rate data is aligned with the portfolio's trading dates before calculating excess returns.

### Visualization

The framework generates a Matplotlib dashboard containing:

* Portfolio value vs. benchmark over time
* Individual portfolio components' value over time
* Strategy performance metrics
* Benchmark performance metrics

<img src="images/Visualization.png" alt="Backtesting performance dashboard" width="800">

---

## Architecture

The framework is divided into several components.

### `data_import.py`

Responsible for retrieving historical market data using `yfinance`.

```python
data_loader(symbols, start_date, end_date)
```

The loader accepts either a single ticker or a list of tickers and returns the corresponding historical data.

---

### `strategy.py`

Contains the strategy classes responsible for calculating derived values and trading signals.

The standard `strategy` class is designed for signals calculated based on singular asset's data, with support for execution of a strategy on multiple assets in the same portfolio.

The multi-asset strategy implementation using `multi_asset_strategy` class allows signals to incorporate information from multiple assets.

<u>This separation allows the same backtesting engine to be used with different trading strategies without changing the portfolio execution code.</u>

---

### `portfolio.py`

Contains the `Backtester` class.

The backtester is responsible for:

1. Initializing the portfolio
2. Processing trading signals
3. Executing buy/sell decisions
4. Updating asset values
5. Recording portfolio history
6. Aggregating multi-asset portfolio values

<u>The execution layer is independent of the strategy definition, making the framework reusable across different signal-generation approaches.</u>

---

### `metrics.py`

Contains the `Metrics` class used to evaluate portfolio performance.

Current metrics include:

| Metric           | Description                                              |
| ---------------- | -------------------------------------------------------- |
| Total Return     | Overall portfolio return over the backtest               |
| Volatility       | Annualized volatility of portfolio returns               |
| Maximum Drawdown | Largest peak-to-trough decline                           |
| Sharpe Ratio     | Annualized risk-adjusted return using the risk-free rate |

---

### `visual.py`

Produces the final performance dashboard using Matplotlib.

The dashboard compares the strategy with its benchmark and displays the calculated performance statistics.

<img src="images/Strategy against benchmark.png" alt="Backtesting performance dashboard" width="800">

---

## Project Structure

```text
backtesting-framework/
│
├── data_import.py
├── strategy.py
├── portfolio.py
├── metrics.py
├── visual.py
├── strategy_and_backtest.py
├── DGS3MO.csv
├── requirements.txt
├── .gitignore
└── README.md
```

`strategy_and_backtest.py` serves as the main user-facing example. It contains the parameters that need to be configured before running a backtest.

---

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/BarKob/backtesting-framework.git
cd backtesting-framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

The main configuration is located in:

```text
strategy_and_backtest.py
```

The user-configurable parameters include:

```python
tickers = []              # str for singular asset, list of strings for multiple assets
start_date = ""           # "YYYY-MM-DD"
end_date = ""             # "YYYY-MM-DD"
benchmark = []            # str for singular asset, list of strings for multiple assets
starting_capital = int    # starting capital
```

A strategy can then be defined using custom value calculations and trading signals.

For example:

```python
Strategy = strategy(
    values={
        "value_name": lambda row: # Equation for a custom value based on the OHLCV data
    },
    signals={
        "signal_name": lambda row: # Statement providing True/False value
    }
)
```

The framework can then be used to:

```text
1. Download historical data
2. Calculate strategy signals
3. Run the backtest
4. Calculate performance metrics
5. Compare the strategy with a benchmark
6. Generate the performance visualization
```

---

## Example Strategy

The framework is strategy-agnostic and does not require a specific trading strategy.

A simple example is a momentum signal based on the 20-day percentage change:

```python
Strategy = strategy(
    values={
        "pct_change_20": lambda row: row["Close"].pct_change(20)
    },
    signals={
        "pct_change_20>0": lambda row: row["pct_change_20"] > 0
    }
)
```

A buy-and-hold benchmark can be represented using the same interface:

```python
Benchmark_Strategy = strategy(
    values={},
    signals={
        "buy&hold": lambda row: True
    }
)
```

<u>The benchmark is therefore evaluated through the same portfolio and performance infrastructure as the strategy rather than being treated as a separate analysis.</u>

---

## Performance Evaluation

The framework evaluates a strategy using both absolute and risk-adjusted measures.

### Total Return

Measures the change in portfolio value between the beginning and end of the backtest.

### Volatility

The standard deviation of daily portfolio returns is annualized to provide a measure of return variability.

### Maximum Drawdown

Maximum drawdown measures the largest decline from a historical portfolio peak.

<u>This provides a direct measure of the downside experienced during the backtest rather than relying solely on total return.</u>

### Sharpe Ratio

The annualized Sharpe ratio is calculated using portfolio excess returns over the daily risk-free rate.

<u>The framework converts the 3-month Treasury yield into a daily rate and aligns the resulting series with the portfolio's trading dates.</u>

---

## Benchmarking

A strategy should not be evaluated solely on whether its portfolio value increased.

The framework therefore supports explicit benchmark comparison.

The benchmark can be configured independently from the strategy and its results are displayed alongside the strategy's:

* Portfolio value
* Total return
* Volatility
* Maximum drawdown
* Sharpe ratio

<img src="images/Metrics comparison.png" alt="Backtesting performance dashboard" width="800">

This makes it possible to assess whether the strategy provides meaningful improvement over a passive alternative.

---

## Design Principles

The project was designed around several principles:

### Modularity

<u>Data loading, strategy logic, portfolio execution, metrics, and visualization are implemented as separate components.</u>

### Strategy Independence

<u>The backtesting engine does not contain strategy-specific trading logic. Strategies provide signals, while the backtester handles execution.</u>

### Extensibility

New strategies can be tested by defining new value calculations and signals without modifying the core portfolio engine.

### Reproducibility

Backtests use explicitly specified:

* Assets
* Start date
* End date
* Initial capital
* Strategy definition
* Benchmark

This makes individual experiments easier to reproduce.

---

## Current Limitations

The framework is intentionally focused on the core mechanics of signal-based backtesting. It currently does not model several features present in production-grade trading systems, including:

* Transaction costs
* Bid-ask spreads
* Slippage
* Market impact
* Position sizing beyond equal initial capital allocation
* Short selling
* Leverage

These limitations mean that the framework should be viewed as a **research and educational backtesting framework rather than a production trading system**.

---

## Future Improvements

Potential extensions include:

* Automated risk-free-rate data acquisition
* Transaction cost and slippage modelling
* More flexible position sizing
* Short positions and leverage
* Portfolio-level risk management
* Additional performance metrics
* Unit and integration testing
* More sophisticated order execution models
* Support for additional market-data providers

---

## Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* yfinance

---

## Project Status

The framework is currently an ongoing personal project focused on developing a modular foundation for systematic trading research.

<u>The project is intentionally implemented without relying on a dedicated quantitative trading/backtesting framework; the core backtesting, portfolio accounting, signal processing, performance metrics, and visualization logic are implemented directly in Python.</u>
