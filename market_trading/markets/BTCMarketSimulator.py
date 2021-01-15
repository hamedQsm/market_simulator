import pandas as pd

from market_trading.markets.MarketBase import MarketBase


class BTCMarketSimulator(MarketBase):
    "return price for every minute"
    def __init__(self, start_timestamp, btc_price_csv):
        super().__init__(start_timestamp)
        btc_df  = pd.read_csv(btc_price_csv)
        self.btc_df= (
            btc_df[btc_df['Timestamp'] > start_timestamp]
            .sort_values('Timestamp', ascending=True)
            .reset_index().drop(columns=['index'])
        )

        self.crnt_index = 0

    def get_current_price(self):
        """
        the price for next minute
        Returns:

        """
        if self.crnt_index >= len(self.btc_df):
            return None

        crnt_row = self.btc_df.iloc[self.crnt_index]
        self.crnt_index += 1
        return {
            'open': crnt_row.Open,
            'close': crnt_row.Close,
            'high': crnt_row.High,
            'low': crnt_row.Low
        }

    def sleep(self, seconds):
        self.crnt_index += seconds//60

    def get_percentage_done(self):
        return int(100*(self.crnt_index)/len(self.btc_df))

    def get_closing_price(self):
        return self.btc_df.iloc[-1].Close
