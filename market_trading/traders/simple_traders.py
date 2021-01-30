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
    # def how_much_to_buy(self, asset_price, price_window=None):
    #     if self.cash_volume == 0:
    #         return 0
    #
    #     if self.asset_volume == 0:
    #         return self.initial_buy_step / asset_price
    #
    #     # loss_margin += self.cash_volume / self.get_account_value(asset_price)
    #     if asset_price < (1 - self.loss_margin) * self.avg_price:
    #         # return self.asset_volume * \
    #         #        (1 - self.loss_margin) / \
    #         #        (self.loss_margin * self.avg_price - asset_price)
    #         # self.loss_margin -= (1 - self.cash_volume / self.get_account_value(asset_price))
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
    #     if self.avg_price < (1 - self.profit_margin)*asset_price:
    #         return self.sell_step/asset_price
    #         # return ((asset_price - self.avg_price )/asset_price) * self.asset_volume
    #     else:
    #         return 0

    def trade(self, price_history, asset_price):
        if (self.cash_volume > 0) and \
                (asset_price < (1 - self.loss_margin) * self.avg_price):
            amount = self.buy_in_currency(self.buy_step, asset_price)
            return 'buy', amount
        elif self.asset_volume > 0 and \
                (self.avg_price < (1 - self.profit_margin)*asset_price):
            amount = self.sell_in_currency(self.sell_step, asset_price)
            return 'sell', amount
        else:
            return None, 0

class WindowTrader(TraderBase):
    def __init__(self,
                 decision_profile,
                 credit, trade_interval,
                 buy_commission, sell_commission):
        super().__init__(credit, trade_interval,
                         buy_commission, sell_commission)
        self.decision_profile = decision_profile
        self.sell_interval = 0
        self.buy_interval = 0


    def trade(self, price_history, asset_price):
        self.sell_interval -= 1 if self.sell_interval > 0 else 0
        self.buy_interval -= 1 if self.buy_interval > 0 else 0
        # if self.asset_volume == 0:
        #     return 'buy', self.initial_buy_step / asset_price
        win_sizes = {ws for _, _, ws, _, _ in self.decision_profile if type(ws) is int}
        mean_win_dict = {
            ws: mean(price_history[-min(ws, len(price_history)):]) for ws in win_sizes
        }
        # TODO: MAYBE look at std as well? if market is fluctuating do not do these?
        for action, amount, win_size, margin, slp_time in self.decision_profile:
            if (action == 'sell' and ((self.asset_volume == 0) or (self.sell_interval > 0))) \
                    or (action == 'buy' and ((self.cash_volume < 0.1) or (self.buy_interval > 0))):
                continue

            take_action = False

            anchor_price = self.avg_price if win_size == 'avg' else mean_win_dict[win_size]
            take_action = (
                (anchor_price < (1 - margin) * asset_price)
                if margin > 0 else (anchor_price > (1 - margin) * asset_price)
            )

            if take_action:
                if action == 'sell':
                    amount = self.sell_in_currency(amount, asset_price)
                    self.sell_interval = slp_time
                    return action, amount
                elif action == 'buy':
                    amount = self.buy_in_currency(amount, asset_price)
                    self.buy_interval = slp_time
                    return action, amount

        return None, 0
