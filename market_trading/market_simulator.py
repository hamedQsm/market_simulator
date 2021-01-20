from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd


class MarketSimulator:
    def __init__(self, market, trader, config):
        self.config = config
        self.trader = trader
        self. market = market

        self.sell_pts = []
        self.buy_pts = []
        self.price_pts = []
        self.cash_pts = []
        self.avg_pts = []
        self.av_pts = []


    def run(self):
        # last_price = self.market.get_current_price()['close']
        # self.trader.initial_buy(last_price)
        # self.buy_pts.append((0, self.trader.initial_credit * self.trader.initial_buy_prcnt / last_price))

        # time_point = 0
        # while True:
        #     # self.market.sleep(self.trader.trade_interval)
        #     price_candle = self.market.get_current_price()
        #
        #     if price_candle is None:
        #         break
        #     else:
        #         price = price_candle['close']
        #         self.price_pts.append(price)
        #         self.av_pts.append(self.trader.get_account_value(price))
        #         self.cash_pts.append(self.trader.cash_volume)
        #
        #     action = None
        #     # TODO: only trader.trade()
        #     buy_vol = self.trader.how_much_to_buy(price, self.price_pts)
        #     if buy_vol > 0:
        #         action_amount = self.trader.buy(buy_vol, price)
        #         self.buy_pts.append((time_point, action_amount))
        #         action = 'Buy'
        #
        #     sell_vol = self.trader.how_much_to_sell(price, self.price_pts)
        #     if sell_vol > 0:
        #         action_amount = self.trader.sell(sell_vol, price)
        #         self.sell_pts.append((time_point, action_amount))
        #         action = 'Sell'
        #
        #     if action:
        #         print(
        #             f'(crnt time: {self.market.crnt_time} - {self.market.get_percentage_done()}%)',
        #             f'{action}: {action_amount:.4f} ',
        #             f'--> AV: {self.trader.get_account_value(price):.4f},'
        #             f'cash: {self.trader.cash_volume:.4f}'
        #         )
        #
        #     time_point += 1

        for time_point, (ts, price_candle) in enumerate(self.market):
            price = price_candle['close']
            self.price_pts.append(price)
            self.av_pts.append(self.trader.get_account_value(price))
            self.cash_pts.append(self.trader.cash_volume)
            self.avg_pts.append(self.trader.avg_price)

            action, amount = self.trader.trade(self.price_pts, price)

            if action:
                if action == 'sell':
                    self.sell_pts.append((time_point, amount))
                elif action == 'buy':
                    self.buy_pts.append((time_point, amount))
                print(
                    f'({datetime.fromtimestamp(ts)} - {self.market.get_percentage_done()}%)',
                    f'{action}: {amount:.4f} ',
                    f'--> AV: {self.trader.get_account_value(price):.4f},'
                    # f'asset: {self.trader.asset_volume:.6f},'
                    f'avg price: {self.trader.avg_price:.2f}',
                    f'cash: {self.trader.cash_volume:.4f}'
                )

            if time_point % 10000 == 0:
                print(datetime.fromtimestamp(ts),
                      f'--> AV: {self.trader.get_account_value(price):.4f}')

        pd.DataFrame({
            # 'config': str(self.config),
            'price':self.price_pts,
            'avg_price': self.avg_pts,
            'portfolio': self.av_pts,
            'cash': self.cash_pts
        }).merge(
            pd.DataFrame(index=[t for t, _ in self.buy_pts], data=[p for _, p in self.buy_pts]),
            left_index=True, right_index=True, how='left'
        ).merge(
            pd.DataFrame(index=[t for t, _ in self.sell_pts], data=[p for _, p in self.sell_pts]),
            left_index=True, right_index=True, how='left'
        ).to_csv(f'../data/sim_res_{self.config}.csv', header=True)

        msp = self.market.get_opening_price()
        mep = self.market.get_closing_price()
        av = self.trader.get_account_value(mep)
        print(
            f'Final account value: {av:.2f}',
            f'Growth: {(av - self.trader.initial_credit)/max(av, self.trader.initial_credit):.2f}'
        )
        print(
            f'Start price: {msp},',
            f'Closing price: {mep},',
            f'Growth: {(mep - msp)/max(mep, msp):.2f}'
        )

    def plot_history(self):
        max_price = max(self.price_pts)
        max_buy_sell = max(
            [y for _, y in self.buy_pts] + [y for _, y in self.sell_pts]
        )

        plt.plot(self.price_pts, label='Price')
        plt.plot(self.av_pts, label='Portfolio')
        plt.plot(self.cash_pts, label='Cash volume')
        plt.plot(self.avg_pts, label='Avg price', ls='--', c='gray')

        plt.vlines([x for x, _ in self.buy_pts],
                   ymin=0, ymax=[.5 * y * max_price / max_buy_sell for _, y in self.buy_pts],
                   lw=.5, colors='green', label='Buy', ls='--', alpha=.6)
        plt.vlines([x for x, _ in self.sell_pts],
                   ymin=[max_price - .5 * y * max_price / max_buy_sell for _, y in self.sell_pts],
                   ymax=max_price,
                   lw=.5, colors='red', label='Sell', ls='--', alpha=.6)

        plt.legend(loc='best')
        plt.show()

