from market_trading.traders.TraderBase import TraderBase


class ATrader(TraderBase):
    def __init__(self,
                buy_step,
                sell_step,
                buy_threshold, 
                sell_threshold,
                buy_threshold_min_def,
                buy_threshold_fast,
                # sleep_after_buy,
                credit, trade_interval, buy_commission, sell_commission):
        super().__init__(credit, trade_interval, buy_commission, sell_commission)

        self.buy_step = buy_step
        self.sell_step = sell_step
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold 
        self.buy_threshold_min_def = buy_threshold_min_def
        # self.sleep_after_buy = sleep_after_buy
        self.trade_interval_orig = trade_interval
        self.buy_threshold_fast = buy_threshold_fast

    def how_much_to_buy(self, asset_price, price_window=None):
        """
        sell enough to drop avg price for `avg_price_down_step`
        Args:
            price_window:
            asset_price:

        Returns:

        """
        if self.avg_price == 0:
            return self.buy_step
        # if asset_price < self.buy_threshold_fast * self.avg_price:
        #     self.trade_interval = self.trade_interval_orig//5
        # else:
        #     self.trade_interval = self.trade_interval_orig

        if asset_price < self.buy_threshold * self.avg_price:
            self.buy_threshold -= (1 - self.cash_volume/self.get_account_value(asset_price)*self.buy_threshold_min_def)
            # TODO: sleep after buy
            return self.buy_step/asset_price
        else:
            return 0


    def how_much_to_sell(self, asset_price, price_window=None):
        """
        if p% in profit then sell p% of the asset volume
        Args:
            price_window:
            asset_price:

        Returns:

        """
        # TODO: need to bring in commission in here
        if self.avg_price < self.sell_threshold*asset_price:
            return self.sell_step/asset_price
        else:
            return 0


    def initial_buy(self, asset_price):
        self.buy_in_currency(self.buy_step, asset_price)