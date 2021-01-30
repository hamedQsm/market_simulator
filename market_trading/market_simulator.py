from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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

        self.axis = None
        self.plot_initiated = False


    def run(self, visualization_win=None):
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

            if action and amount > 0:
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

            if visualization_win:
                if time_point % (visualization_win//10) == 0:
                    self.plot(visualization_win)

        msp = self.market.get_opening_price()
        mep = self.market.get_closing_price()
        av = self.trader.get_account_value(mep)
        print(
            f'Final account value: {av:.2f}',
            f'Growth: {100*(av - self.trader.initial_credit)/self.trader.initial_credit:.2f}',
            f'Commission payed: {self.trader.commission_payed:.2f}%'
        )
        print(
            f'Start price: {msp},',
            f'Closing price: {mep},',
            f'Growth: {100*(mep - msp)/msp:.2f}%'
        )


    def save_results(self):
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

    def plot_all_history(self):
        plt.ioff()
        self.axis = None
        self.plot()

    def plot(self, steps=None):
        if steps is None:
            steps = len(self.price_pts)
            dynamic = False
        else:
            dynamic = True
        if steps > len(self.price_pts):
            return
        # steps = min(steps, len(self.price_pts))
        x_pts = list(range(len(self.price_pts) - steps, len(self.price_pts)))
        prc_pts = self.price_pts[-steps:]
        avg_pts = self.avg_pts[-steps:]
        cash_pts = self.cash_pts[-steps:]
        av_pts = self.av_pts[-steps:]
        sell_pts = [(x, y) for x, y in self.sell_pts if x in x_pts]
        buy_pts = [(x, y) for x, y in self.buy_pts if x in x_pts]

        max_price = max(self.price_pts)

        if len(sell_pts) + len(buy_pts) > 0:
            max_buy_sell = max(
                [y for _, y in buy_pts] + [y for _, y in sell_pts]
            )
        else:
            max_buy_sell = 1

        if self.axis is None:
            if dynamic:
                plt.ion()
            fig = plt.figure(figsize=(12, 7))
            self.axis = fig.add_subplot(111)
            self.price_plt = self.axis.plot(x_pts, prc_pts, label='Price')[0]
            self.porto_plt = self.axis.plot(av_pts, label='Portfolio')[0]
            self.cash_plt = self.axis.plot(cash_pts, label='Cash volume')[0]
            self.avg_plt = self.axis.plot(x_pts, avg_pts, label='Avg price', ls='--', c='gray')[0]

            self.buy_lines = plt.vlines([x for x, _ in buy_pts],
                                        ymin=0, ymax=[.5 * y * max_price / max_buy_sell for _, y in buy_pts],
                                        lw=.5, colors='green', label='Buy', ls='--', alpha=.6)
            self.sell_lines = plt.vlines([x for x, _ in sell_pts],
                                         ymin=[max_price - .5 * y * max_price / max_buy_sell for _, y in sell_pts],
                                         ymax=max_price,
                                         lw=.5, colors='red', label='Sell', ls='--', alpha=.6)
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.show()

            return

        plt.xlim([x_pts[0], x_pts[-1]])
        self.price_plt.set_data(x_pts, prc_pts)
        self.porto_plt.set_data(x_pts, av_pts)
        self.cash_plt.set_data(x_pts, cash_pts)
        self.avg_plt.set_data(x_pts, avg_pts)

        self.buy_lines = plt.vlines([x for x, _ in buy_pts],
                                    ymin=0, ymax=[.5 * y * max_price / max_buy_sell for _, y in buy_pts],
                                    lw=.5, colors='green', ls='--', alpha=.6)
        self.sell_lines = plt.vlines([x for x, _ in sell_pts],
                                     ymin=[max_price - .5 * y * max_price / max_buy_sell for _, y in sell_pts],
                                     ymax=max_price,
                                     lw=.5, colors='red', ls='--', alpha=.6)

        # adjust limits if new data goes beyond bounds
        # if min(prc_pts) <= self.price_plt.axes.get_ylim()[0] or \
        #         max(prc_pts) >= self.price_plt.axes.get_ylim()[1]:
        plt.ylim([0 , max([x for x in prc_pts if ~np.isnan(x)])])
        #
        #
        plt.title(f'({self.market.get_percentage_done()}%)')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.pause(.0001)

        # plt.savefig(f"../data/res_{self.config}.png")
