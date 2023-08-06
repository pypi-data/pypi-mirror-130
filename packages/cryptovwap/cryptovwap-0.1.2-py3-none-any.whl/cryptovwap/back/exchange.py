from abc import abstractmethod, abstractproperty
from abc import ABCMeta
from .helpers import *

class Exchange(metaclass=ABCMeta):

    @property
    @abstractmethod
    def exchange_name(self):
        pass

    @property
    @abstractmethod
    def default_trade(self):
        pass

    @abstractmethod
    def get_data(self, symbol, since=None, to=None):
        pass

    @abstractmethod
    def get_asset_pairs(self):
        pass

    @abstractmethod
    def get_asset_pairs_symbols(self):
        pass

    @staticmethod
    def vwap(df, fvwap):
        filtro = FREQ_VWAP[fvwap]

        df = df.copy()
        df["vwap"] = df["price"] * df["volume"]
        df["time"] = df["time"].apply(lambda x: generate_filter(x, filtro))
        df = df.groupby('time').agg({'price': 'mean', 'volume': 'sum', 'vwap': 'sum'}).reset_index()
        df["vwap"] = df["vwap"] / df["volume"]

        return df