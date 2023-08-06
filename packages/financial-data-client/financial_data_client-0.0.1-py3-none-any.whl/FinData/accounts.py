from kucoin.client import User as KucoinUser
from kucoin.client import Market as KucoinData
from binance import Client as BinanceClient
from FinData.constants import *
import datetime
import pandas as pd
import time


class AccountAPI:

    def __init__(self, account_params):
        
        self.account_params = account_params
        self.account_type = None

    def get_bars(self, bar_type, first_bar_datetime, last_bar_datetime=None):

        pass

    def convert_symbol(self, symbol):

        pass

    def convert_bar_type(self, bar_type):

        pass

    @staticmethod
    def fromAccountParams(account_name, account_params):

        if account_name == "KUCOIN":
            return KucoinAPI(account_params)
        elif account_name == "BINANCE":
            return BinanceAPI(account_params)


class KucoinAPI(AccountAPI):

    def __init__(self, account_params):
        super().__init__(account_params)
        self.data_client = KucoinData(self.account_params["KUCOIN_API_KEY"], self.account_params["KUCOIN_API_SECRET"], self.account_params["KUCOIN_API_PASSPHRASE"])
        self.user_client = KucoinUser(self.account_params["KUCOIN_API_KEY"], self.account_params["KUCOIN_API_SECRET"], self.account_params["KUCOIN_API_PASSPHRASE"])
        self.account_type = "crypto"

    def convert_symbol(self, symbol):
        
        symbol = symbol.upper()
        if symbol[-3:] == "USD" and "-" not in symbol:
            return symbol[:-3] + "-USDT"
        elif symbol[-4:] == "USDT" and "-" not in symbol:
            return symbol[:-4] + "-USDT"

    def convert_bar_type(self, bar_type):
        
        return bar_type
    
    def get_bars(self, symbol, bar_type, first_bar_datetime, last_bar_datetime):
        
        symbol = self.convert_symbol(symbol)
        bar_type = self.convert_bar_type(bar_type)
        bars = []
        end = int(datetime.datetime(last_bar_datetime.year, last_bar_datetime.month, last_bar_datetime.day, last_bar_datetime.hour, last_bar_datetime.minute, 0).timestamp())
        first_ts = int(datetime.datetime(first_bar_datetime.year, first_bar_datetime.month, first_bar_datetime.day, first_bar_datetime.hour, first_bar_datetime.minute, 0).timestamp())
        while end >= first_ts:
            start = end - (KUCOIN_FRAME_CONV[bar_type]*1500)
            try:
                data = self.data_client.get_kline(symbol, bar_type, startAt=start, endAt=end)
            except:
                time.sleep(1)
                continue
            bars += data
            end = start

        df = pd.DataFrame(bars, columns=["time","kucoin_open","kucoin_close","kucoin_high","kucoin_low","kucoin_count","kucoin_vol"])
        df["time"] = df["time"].astype(int)
        for col in ["kucoin_open","kucoin_close","kucoin_high","kucoin_low","kucoin_count","kucoin_vol"]:
            df[col] = df[col].astype(float)
        df["time"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(x))
        df = df.sort_values("time").reset_index(drop=True)
        df = df[(df["time"] >= first_bar_datetime) & (df["time"] <= last_bar_datetime)]
        return df


class BinanceAPI(AccountAPI):

    def __init__(self, account_params):
        super().__init__(account_params)
        all_client = self.client = BinanceClient(self.account_params["BINANCE_API_KEY"], self.account_params["BINANCE_API_SECRET"], tld="us")
        self.data_client = all_client
        self.user_client = all_client
        self.account_type = "crypto"

    def convert_symbol(self, symbol):
        
        return symbol

    def convert_bar_type(self, bar_type):
        
        return bar_type.replace("min", "m")


    def get_bars(self, symbol, bar_type, first_bar_datetime, last_bar_datetime):
        
        bar_type = self.convert_bar_type(bar_type)
        end = int(datetime.datetime(last_bar_datetime.year, last_bar_datetime.month, last_bar_datetime.day, last_bar_datetime.hour, last_bar_datetime.minute, 0).timestamp() * 1000)
        first_ts = int(datetime.datetime(first_bar_datetime.year, first_bar_datetime.month, first_bar_datetime.day, first_bar_datetime.hour, first_bar_datetime.minute, 0).timestamp() * 1000)

        bars = []
        while end >= first_ts:
            data = self.data_client.get_klines(symbol=symbol, interval=BINANCE_INTERVALS[bar_type], limit=1000, endTime=end)
            bars += data
            end = data[0][0]
        
        df = pd.DataFrame(bars, columns=["time","binance_open","binance_high","binance_low","binance_close","binance_vol","close_time","binance_count","binance_count","binance_buy_base_vol","binance_buy_quote_vol","ignore"])
        df["time"] = df["time"].astype(int)
        for col in ["binance_open","binance_high","binance_low","binance_close","binance_vol","close_time","binance_count","binance_count","binance_buy_base_vol","binance_buy_quote_vol"]:
            df[col] = df[col].astype(float)
        df["time"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(int(str(x)[:-3])))
        df = df.sort_values("time").reset_index(drop=True)
        df = df[(df["time"] >= first_bar_datetime) & (df["time"] <= last_bar_datetime)]
        return df[["time","binance_open","binance_high","binance_low","binance_close","binance_vol","binance_count"]]