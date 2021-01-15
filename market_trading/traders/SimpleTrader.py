from market_trading.traders.TraderBase import TraderBase


class SimpleTrader(TraderBase):
    def __init__(self,
                 # price_drop_thrshold,
                 # price_raise_threshold,
                 # max_buy_prcnt,
                 initial_buy_prcnt,
                 profit_margin,
                 avg_price_down_step,
                 credit, trade_interval, buy_commission, sell_commission):
        super().__init__(credit, trade_interval, buy_commission, sell_commission)

        # self.profit_margin = profit_margin
        self.profit_margin = profit_margin
        self.avg_price_down_step = avg_price_down_step
        # self.max_credit_prcnt = max_buy_prcnt
        self.initial_buy_prcnt = initial_buy_prcnt
        # self.price_raise_threshold = price_raise_threshold
        # self.price_drop_thrshold = price_drop_thrshold

    def how_much_to_buy(self, asset_price):
        """
        sell enough to drop avg price for `avg_price_down_step`
        Args:
            asset_price:

        Returns:

        """
        if self.avg_price == 0:
            return self.cash_volume * self.initial_buy_prcnt / asset_price

        if asset_price < self.avg_price_down_step * self.avg_price:
            return self.asset_volume*\
                   (1 - self.avg_price_down_step)/(self.avg_price_down_step * self.avg_price - asset_price)
        else:
            return 0


    def how_much_to_sell(self, asset_price):
        """
        if p% in profit then sell p% of the asset volume
        Args:
            asset_price:

        Returns:

        """
        # TODO: need to bring in commission in here
        if self.avg_price < self.profit_margin*asset_price:
            return ((asset_price - self.avg_price )/asset_price) * self.asset_volume
        else:
            return 0


    def initial_buy(self, asset_price):
        self.buy_in_currency(self.cash_volume * self.initial_buy_prcnt, asset_price)