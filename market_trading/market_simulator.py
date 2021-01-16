import matplotlib.pyplot as plt


class MarketSimulator:
    def __init__(self, market, trader):
        self.trader = trader
        self. market = market

        self.sell_pts = []
        self.buy_pts = []
        self.price_pts = []
        self.cash_pts = []
        self.av_pts = []

    def run(self):
        # last_price = self.market.get_current_price()['close']
        # self.trader.initial_buy(last_price)
        # self.buy_pts.append((0, self.trader.initial_credit * self.trader.initial_buy_prcnt / last_price))

        time_point = 0
        while True:
            # self.market.sleep(self.trader.trade_interval)
            price_candle = self.market.get_current_price()

            if price_candle is None:
                break
            else:
                price = price_candle['close']
                self.price_pts.append(price)
                self.av_pts.append(self.trader.get_account_value(price))
                self.cash_pts.append(self.trader.cash_volume)

            action = None
            buy_vol = self.trader.how_much_to_buy(price, self.price_pts)
            if buy_vol > 0:
                action_amount = self.trader.buy(buy_vol, price)
                self.buy_pts.append((time_point, action_amount))
                action = 'Buy'

            sell_vol = self.trader.how_much_to_sell(price, self.price_pts)
            if sell_vol > 0:
                action_amount = self.trader.sell(sell_vol, price)
                self.sell_pts.append((time_point, action_amount))
                action = 'Sell'

            if action:
                print(
                    f'(crnt time: {self.market.crnt_time} - {self.market.get_percentage_done()}%)',
                    f'{action}: {action_amount:.4f} ',
                    f'--> AV: {self.trader.get_account_value(price):.4f},'
                    f'cash: {self.trader.cash_volume:.4f}'
                )

            time_point += 1

        print(f'Final account value: {self.trader.get_account_value(self.market.get_closing_price())}')

    def plot_history(self):
        max_price = max(self.price_pts)
        max_buy_sell = max(
            [y for _, y in self.buy_pts] + [y for _, y in self.sell_pts]
        )

        plt.plot(self.price_pts, label='Price')
        plt.plot(self.av_pts, label='Portfolio')
        plt.plot(self.cash_pts, label='Cash volume')

        plt.vlines([x for x, _ in self.buy_pts],
                   ymin=0, ymax=[y * max_price / max_buy_sell for _, y in self.buy_pts],
                   lw=1, colors='green', label='Buy', ls='--')
        plt.vlines([x for x, _ in self.sell_pts],
                   ymin=0, ymax=[y * max_price / max_buy_sell for _, y in self.sell_pts],
                   lw=1, colors='red', label='Sell', ls='--')

        plt.legend(loc='best')
        plt.show()

