import pandas as pd

from data_import import data_loader

class strategy:

    def __init__(self, values, signals):
        self.values = values
        self.signals = signals

    def calculate_values(self, data: dict):
        for asset in data:
            for value, equation in self.values.items():
                data[asset][value] = equation(data[asset])
        return data

    def calculate_signal(self, data: dict):
        self.calculate_values(data)
        for asset in data:
            for signal_name, f in self.signals.items():
                data[asset][signal_name] = f(data[asset])

            data[asset]["signal"] = data[asset][self.signals.keys()].all(axis=1)
        return data

class multi_asset_startegy:

    def __init__(self, assets_to_trade, values, signals):
        self.values = values
        self.signals = signals
        self.assets_to_trade = assets_to_trade

    def calculate_values(self, data: dict):
        for asset in data:
            for value, equation in self.values.items():
                data[asset][value] = equation(data[asset])
        return data

    def calculate_signal(self, data: dict):
        self.calculate_values(data)
        for asset in self.assets_to_trade:
            for signal_name, f in self.signals.items():
                data[asset][signal_name] = f(data)
            data[asset]["signal"] = data[asset][self.signals.keys()].all(axis=1)
        data_new = {asset_name:dataframe for asset_name, dataframe in data.items() if asset_name in self.assets_to_trade}
        return data_new

        