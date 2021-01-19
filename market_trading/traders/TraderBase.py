class TraderBase:
    def __init__(self, credit, trade_interval, buy_commission, sell_commision):
        self.sell_commision = sell_commision
        self.buy_commission = buy_commission
        self.avg_price = 0
        self.asset_volume = 0
        self.initial_credit=credit
        self.cash_volume = credit
        self.trade_interval = trade_interval

    def buy(self, asset_vol, asset_price):
        """

        Args:
            asset_vol:
            asset_price:

        Returns:
            price paid
        """
        needed_cash_vol = min(
            self.cash_volume,
            (asset_vol * asset_price) * (1 + self.buy_commission)
        )
        self.avg_price = \
            (self.avg_price * self.asset_volume + asset_price * asset_vol) / (self.asset_volume + asset_vol)
        self.cash_volume -= needed_cash_vol
        # correction needed in case we do not have enough cash to buy asked asset volume
        self.asset_volume += (needed_cash_vol/(1 + self.buy_commission))/asset_price
        return needed_cash_vol

    def sell(self, asset_vol, asset_price):
        """

        Args:
            asset_vol:
            asset_price:

        Returns:
            credits earned
        """
        asset_vol = min(self.asset_volume, asset_vol)
        cash_back = (asset_vol * asset_price) * (1 - self.sell_commision)
        self.cash_volume += cash_back
        self.asset_volume -= asset_vol
        if self.asset_volume == 0:
            self.avg_price = 0
        return cash_back


    def buy_in_currency(self, amount, asset_price):
        return self.buy(amount/asset_price, asset_price)

    def sell_in_currency(self, amount, asset_price):
        return self.sell(amount/asset_price, asset_price)

    # def how_much_to_buy(self, asset_price, price_window=None):
    #     """ Will be called in every simulation step
    #
    #     Args:
    #         price_window:
    #     """
    #     pass
    #
    # def how_much_to_sell(self, asset_price, price_window=None):
    #     """ Will be called in every simulation step
    #
    #     Args:
    #         price_window:
    #     """
    #     pass

    def initial_buy(self, asset_price):
        """ How much to buy at the very beginning of the trade"""
        pass

    def trade(self, price_history, asset_price):
        pass

    def get_account_value(self, price):
        return (self.cash_volume + self.asset_volume*price)
