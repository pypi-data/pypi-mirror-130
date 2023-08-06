import json
import os
from FinData.constants import *
from FinData.accounts import *
from functools import reduce

class FinancialDataClient:

    def __init__(self, accounts, accounts_json_path=None):
        
        self.kucoin_api = None
        self.binance_api = None
        self.accounts = []

        if accounts_json_path != None:
            accounts_values = json.load(open(accounts_json_path))
        else:
            accounts_values = {account: {key: os.getenv(key) for key in ACCOUNT_CLIENT_PARAMS[account]} for account in accounts}
        for account in accounts:
            self.accounts.append(AccountAPI.fromAccountParams(account, accounts_values[account]))
        
    
    def get_bars(self, account_type, symbol, bar_type, first_bar_datetime, last_bar_datetime=None):
        
        if last_bar_datetime == None:
            last_bar_datetime = datetime.datetime.today()
        dfs = []
        for account in self.accounts:
            if account.account_type == account_type:
                dfs.append(account.get_bars(symbol, bar_type, first_bar_datetime, last_bar_datetime))
        df_merged = reduce(lambda  left,right: pd.merge(left, right, on=['time'],how='inner'), dfs)
        return df_merged
        