from datetime import datetime

from market_trading.market_simulator import MarketSimulator
from market_trading.markets.BTCMarketSimulator import BTCMarketSimulator
from market_trading.traders.simple_traders import AVGTrader, WindowTrader

CREDIT = 1000
BUY_COMMISSION = .01
SELL_COMMISSION = .01

CONFIG = {
    'sleep_time': 60 * 5,
    # list of windows: (what_to_do, amount, window_size in min, profit_margin)
    # ORDER MATTERS: the list elements are considered in order.
    'decision_profile': [
        # risk aversion: if we have a huge drop we want to sell to avert big loss.
        # ('sell', 30, 30, -.1),
        ('sell', 40, 24*60, -.15),
        #('sell', 100, 30*24*60, -.2),

        # lowering average
        ('buy', 10, 30, -.02), #('buy', 20, 24*60, -.05),  ('buy', 50, 30*24*60, -.1),

         # sell in case of profit
        ('sell', 10, 30, .04),
        ('sell', 20, 24*60, .05),
        #('sell', 50, 30*24*60, .1)

    ],
}

def run_simulation():
    market = BTCMarketSimulator(
        start_timestamp=int(datetime(year=2017, month=11, day=1).timestamp()),
        end_timestamp=int(datetime(year=2018, month=6, day=1).timestamp()),
        btc_price_csv='../data/bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv'
    )

    # trader = AVGTrader(
    #     initial_buy_step=initial_buy,
    #     sell_step=sell_step,
    #     loss_margin=loss_margin,
    #     profit_margin=profit_margin,
    #     credit=CREDIT,
    #     trade_interval=sleep_time,
    #     buy_commission=BUY_COMMISSION,
    #     sell_commission=SELL_COMMISSION
    # )

    trader = WindowTrader(
        decision_profile=CONFIG['decision_profile'],
        credit=CREDIT,
        trade_interval=CONFIG["sleep_time"],
        buy_commission=BUY_COMMISSION,
        sell_commission=SELL_COMMISSION
    )

    simulation = MarketSimulator(market, trader, CONFIG)

    simulation.run()

    simulation.plot_history()

if __name__ == '__main__':
    run_simulation()




