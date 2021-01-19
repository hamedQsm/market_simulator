from statistics import mean

from market_trading.traders.TraderBase import TraderBase

class SimpleTrader(TraderBase):
    def __init__(self,
                 # price_drop_thrshold,
                 # price_raise_threshold,
                 # max_buy_prcnt,
                 initial_buy_step,
                 sell_step,
                 profit_margin,
                 loss_margin,
                 credit, trade_interval, buy_commission, sell_commission):
        super().__init__(credit, trade_interval, buy_commission, sell_commission)

        # self.profit_margin = profit_margin
        self.profit_margin = profit_margin
        self.loss_margin = loss_margin
        # self.max_credit_prcnt = max_buy_prcnt
        self.initial_buy_step = initial_buy_step
        self.buy_step = initial_buy_step
        self.sell_step = sell_step
        # self.price_raise_threshold = price_raise_threshold
        # self.price_drop_thrshold = price_drop_thrshold


class AVGTrader(SimpleTrader):
    def how_much_to_buy(self, asset_price, price_window=None):
        if self.cash_volume == 0:
            return 0

        if self.asset_volume == 0:
            return self.initial_buy_step / asset_price

        # loss_margin += self.cash_volume / self.get_account_value(asset_price)
        if asset_price < (1 - self.loss_margin) * self.avg_price:
            # return self.asset_volume * \
            #        (1 - self.loss_margin) / \
            #        (self.loss_margin * self.avg_price - asset_price)
            # self.loss_margin -= (1 - self.cash_volume / self.get_account_value(asset_price))
            return self.buy_step / asset_price
        else:
            return 0


    def how_much_to_sell(self, asset_price, price_window=None):

        if self.asset_volume == 0:
            return 0
        # TODO: need to bring in commission in here
        if self.avg_price < (1 - self.profit_margin)*asset_price:
            return self.sell_step/asset_price
            # return ((asset_price - self.avg_price )/asset_price) * self.asset_volume
        else:
            return 0


    def initial_buy(self, asset_price):
        self.buy_in_currency(self.cash_volume * self.initial_buy_prcnt, asset_price)


class WindowTrader(SimpleTrader):
    def __init__(self, buy_win_size, sell_win_size, initial_buy_step, sell_step,
                 profit_margin, loss_margin, loss_aversion_margin, credit, trade_interval,
                 buy_commission, sell_commission):
        super().__init__(initial_buy_step, sell_step,
                         profit_margin, loss_margin, credit, trade_interval,
                         buy_commission, sell_commission)

        self.loss_aversion_margin = loss_aversion_margin
        self.buy_win_size = buy_win_size
        self.sell_win_size = sell_win_size


    # def how_much_to_buy(self, asset_price, price_window=None):
    #     if self.cash_volume == 0:
    #         return 0
    #
    #     if self.asset_volume == 0:
    #         return self.initial_buy_step / asset_price
    #     win_index = min(self.buy_win_size, len(price_window))
    #     if asset_price < (1 - self.loss_margin) * mean(price_window[-win_index:]):
    #         return self.buy_step / asset_price
    #     else:
    #         return 0
    #
    #
    # def how_much_to_sell(self, asset_price, price_window=None):
    #
    #     if self.asset_volume == 0:
    #         return 0
    #     # TODO: need to bring in commission in here
    #     win_index = min(self.sell_win_size, len(price_window))
    #     if (mean(price_window[-win_index:]) < (1 - self.profit_margin)*asset_price)  \
    #         or (self.avg_price > (1 - self.loss_aversion_margin)*asset_price):
    #         return self.sell_step/asset_price
    #         # return ((asset_price - self.avg_price )/asset_price) * self.asset_volume
    #     else:
    #         return 0

    def trade(self, price_history, asset_price):
        # if self.asset_volume == 0:
        #     return 'buy', self.initial_buy_step / asset_price

        buy_win_index = min(self.buy_win_size, len(price_history))
        sell_win_index = min(self.sell_win_size, len(price_history))

        if (self.cash_volume > 0) and \
                (asset_price < (1 - self.loss_margin) * mean(price_history[-buy_win_index:])):
            amount = self.buy_in_currency(self.buy_step, asset_price)
            return 'buy', amount
        elif self.asset_volume > 0 and \
                (
                    (mean(price_history[-sell_win_index:]) < (1 - self.profit_margin)*asset_price)  #or
                    # (self.avg_price > (1 - self.loss_aversion_margin)*asset_price)
                ):
            amount = self.sell_in_currency(self.sell_step, asset_price)
            return 'sell', amount
        else:
            return None, 0