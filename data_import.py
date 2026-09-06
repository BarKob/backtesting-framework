import yfinance as yf

class data_loader:

    def __init__(self, symbols: str | list, start_date, end_date):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date

    def load_data(self):
        if isinstance(self.symbols, list):
            data = {symbol: yf.download(tickers = symbol, start = self.start_date, end = self.end_date, multi_level_index = False) for symbol in self.symbols}
        else:
            data = {self.symbols: yf.download(tickers = self.symbols, start = self.start_date, end = self.end_date, multi_level_index = False)}
        return data

        


