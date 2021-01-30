import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle as pkl

import tensorflow as tf

tfk = tf.keras
tfkl = tf.keras.layers

from market_trading.traders.TraderBase import TraderBase


class LSTMTrader(TraderBase):
    def __init__(self, credit, trade_interval, buy_commission, sell_commission,
                 model_path, scalar_path):
        super().__init__(credit, trade_interval, buy_commission, sell_commission)

        self.model = tfk.models.load_model(model_path)
        self.scalar = pkl.load(open(scalar_path, 'rb'))
        self.train_interval = 60
        self.train_win = 60
        self.time_to_trade = self.train_win * self.trade_interval

    def trade(self, price_history, asset_price):
        if self.time_to_trade > 0:
            self.time_to_trade -= 1
            return None, 0

        n = self.train_win*self.train_interval
        prices = np.array(
            price_history[-n:]
        ).reshape(-1, 1)

        indices = [i for i in range(0, n, self.train_interval)]
        data = prices[indices, :]
        next_price_pred = self.scalar.inverse_transform(
            self.model.predict(
                self.scalar.transform(data).reshape(1, self.train_win, 1)
            )
        )[0][0]

        self.time_to_trade = self.trade_interval
        # print(f'asset price: {asset_price:.3f}, next price predicted: {next_price_pred:.3f}')
        if (asset_price - next_price_pred)/asset_price > .01:
            amount = self.sell_in_currency(5, asset_price)
            return 'sell', amount
        elif (next_price_pred - asset_price)/next_price_pred > .01 :
            amount = self.buy_in_currency(5, asset_price)
            return 'buy', amount
        else:
            return None, 0



