import matplotlib.pyplot as plt


class MarketSimulator:
    def __init__(self, market, trader):
        self.trader = trader
        self. market = market

        self.sell_pts = []
        self.buy_pts = []
        self.price_pts = []

    def run(self):
        last_price = self.market.get_current_price()['close']
        self.trader.initial_buy(last_price)
        self.buy_pts.append((0, self.trader.initial_credit * self.trader.initial_buy_prcnt / last_price))

        time_point = 0
        while True:
            self.market.sleep(self.trader.trade_interval)
            price_candle = self.market.get_current_price()

            if price_candle is None:
                break
            else:
                price = price_candle['close']
                self.price_pts.append(price)

            buy_vol = self.trader.how_much_to_buy(price)

            if buy_vol > 0:
                paid = self.trader.buy(buy_vol, price)
                self.buy_pts.append((time_point, buy_vol))
                print(
                    f'Bought: {paid} '
                    f'--> account value: {self.trader.get_account_value(price)}'
                    f'({self.market.get_percentage_done()}%)'
                )

            sell_vol = self.trader.how_much_to_sell(price)
            if sell_vol > 0:
                earned = self.trader.sell(sell_vol, price)
                self.sell_pts.append((time_point, sell_vol))
                print(
                    f'Sold: {earned} '
                    f'--> account value: {self.trader.get_account_value(price)}'
                    f'({self.market.get_percentage_done()}%)'
                )

            time_point += 1

        print(f'Final account value: {self.trader.get_account_value(self.market.get_closing_price())}')

    def plot_history(self):
        max_price = max(self.price_pts)
        max_buy = max([y for _, y in self.buy_pts])
        max_sell = max([y for _, y in self.sell_pts])
        plt.plot(self.price_pts, label='Price')
        plt.vlines([x for x, _ in self.buy_pts],
                   ymin=0, ymax=[y * max_price / max_buy for _, y in self.buy_pts],
                   lw=2, colors='green', label='Buy')
        plt.vlines([x for x, _ in self.sell_pts],
                   ymin=0, ymax=[y * max_price / max_sell for _, y in self.sell_pts],
                   lw=2, colors='red', label='Sell')

        plt.legend(loc='best')
        plt.show()

