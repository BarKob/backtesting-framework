import pandas as pd
import numpy as np

class Metrics:

    def __init__(self, portfolio_history: dict):
        self.portfolio_history = portfolio_history
        self.daily_portfolio_values = portfolio_history["Total_Portfolio_Value"]
        self.rfr_with_portfolio_values = pd.DataFrame()
        
    def risk_free_download_join(self, csv_source = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO"):
        risk_free_rates = pd.read_csv(csv_source, index_col = "observation_date").ffill()
        risk_free_rates.index = pd.to_datetime(risk_free_rates.index).normalize()
        risk_free_rates["DGS3MO"] = (risk_free_rates["DGS3MO"] / 100 + 1) ** (1 / 252) - 1
        self.rfr_with_portfolio_values = self.daily_portfolio_values.to_frame().join(risk_free_rates, how = "left")

    def calculate_metrics(self):
        total_return_pct = self.daily_portfolio_values.iloc[-1] / self.daily_portfolio_values.iloc[0] - 1

        returns_pct = self.daily_portfolio_values.pct_change().dropna()
        volatility = returns_pct.std() * np.sqrt(len(returns_pct))

        previous_peak = self.daily_portfolio_values.cummax()
        drawdown = self.daily_portfolio_values / previous_peak - 1
        max_drawdown = drawdown.min()

        self.risk_free_download_join()
        excess_returns = pd.Series(returns_pct) - self.rfr_with_portfolio_values["DGS3MO"]
        sharpe_ann = (excess_returns.mean() / returns_pct.std()) * (np.sqrt(252))

        print(total_return_pct, volatility, max_drawdown, sharpe_ann)
        metrics = {"Total return":total_return_pct,  
                   "Volatility":volatility, 
                   "Maximum Drawdown":max_drawdown, 
                   "Sharpe ratio":sharpe_ann}
        return metrics
