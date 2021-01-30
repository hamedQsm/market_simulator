class TraderBase:
    def __init__(self, credit, trade_interval, buy_commission, sell_commission):
        self.sell_commision = sell_commission
        self.buy_commission = buy_commission
        self.avg_price = 0
        self.asset_volume = 0
        self.initial_credit=credit
        self.cash_volume = credit
        self.trade_interval = trade_interval
        self.commission_payed = 0
        self.current_profit = 0

    def update_profit(self, asset_price):
        av = self.get_account_value(asset_price)
        self.current_profit = (av - self.initial_credit) / self.initial_credit

    def buy(self, asset_vol, asset_price):
        """

        Args:
            asset_vol:
            asset_price:

        Returns:
            price paid
        """
        payable_cash = (asset_vol * asset_price) * (1 + self.buy_commission)

        if self.cash_volume < payable_cash:
            payable_cash = self.cash_volume * (1 - self.buy_commission)
            asset_vol = payable_cash / asset_price

        if payable_cash > 0:
            self.avg_price = \
                (self.avg_price * self.asset_volume + asset_price * asset_vol) / (self.asset_volume + asset_vol)
            self.cash_volume -= payable_cash
            # correction needed in case we do not have enough cash to buy asked asset volume
            self.asset_volume += asset_vol
            self.commission_payed += self.buy_commission

        return  payable_cash

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
        if asset_vol > 0:
            self.commission_payed += self.sell_commision
        return cash_back


    def buy_in_currency(self, amount, asset_price):
        return self.buy(amount/asset_price, asset_price)

    def sell_in_currency(self, amount, asset_price):
        return self.sell(amount/asset_price, asset_price)

    def initial_buy(self, asset_price):
        """ How much to buy at the very beginning of the trade"""
        pass

    def trade(self, price_history, asset_price):
        pass

    def get_account_value(self, price):
        return (self.cash_volume + self.asset_volume*price)
