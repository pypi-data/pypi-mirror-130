from python_bitvavo_api.bitvavo import Bitvavo as Bv
import pandas as pd
from .exchange import Exchange


class Bitvavo(Exchange):

    @property
    def exchange_name(self):
        return "Bitvavo"

    @property
    def default_trade(self):
        return "ADA-EUR"

    def __init__(self):
        self.bitvavo = Bv({
            'RESTURL': 'https://api.bitvavo.com/v2',
            'WSURL': 'wss://ws.bitvavo.com/v2/',
            'ACCESSWINDOW': 10000,
            'DEBUGGING': False
        })

    def get_data(self, symbol, since=None, to=None):
        if since is None and to is None:
            df = pd.DataFrame(self.bitvavo.publicTrades(symbol, {"limit": 1000}))
            df = self._prepare_df(symbol, df)
        else:
            minus = to
            dfs = []
            while minus > since:
                df = self._prepare_df(symbol, pd.DataFrame(
                    self.bitvavo.publicTrades(symbol, {"limit": 1000, "end": str(int(minus * 1000))})))
                minus = min(df["time"])
                dfs.append(df)
            df = pd.concat(dfs)
            df = df[df["time"].between(since, to)].reset_index(drop=True)

        return df

    def _prepare_df(self, symbol, df):
        data = df.copy()
        data.columns = ["id", "time", "volume", "price", "side"]

        data["symbol"] = symbol
        data["volume"] = data["volume"].astype(float)
        data["price"] = data["price"].astype(float)
        data["time"] = data["time"] / 1000

        return data[["symbol", "price", "volume", "time"]]

    def get_asset_pairs(self):
        return [tuple(x.split("-")) for x in self.get_asset_pairs_symbols()]

    def get_asset_pairs_symbols(self):
        return [x["market"] for x in self.bitvavo.markets({})]
