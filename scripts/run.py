from datetime import datetime
from itertools import product

from market_trading.market_simulator import MarketSimulator
from market_trading.markets.BTCMarketSimulator import BTCMarketSimulator
from market_trading.traders.ml_traders import LSTMTrader
from market_trading.traders.simple_traders import AVGTrader, WindowTrader

CREDIT = 1000
BUY_COMMISSION = .01
SELL_COMMISSION = .01

CONFIG = {
    'sleep_time': 60 * 5,
    # list of windows: (what_to_do, amount, window_size in min, profit_margin, sleep_time in min)
    # ORDER MATTERS: the list elements are considered in order.
    'decision_profile': [
        # risk aversion: if we have a huge drop we want to sell to avert big loss.
        # ('sell', 10, 30, -.02, 5),
        # ('sell', 30, 60, -.1, 20),
        # ('sell', 40, 2*60, -.15, 30),
        # ('sell', 60, 4*60, -.2, 60),
        # ('sell', 40, 24*60, -.1),
        # ('sell', 60, 24*60, -.15),
        # ('sell', 100, 30*24*60, -.2),

        # if in good profit sell
        ('sell', 200, 'avg', .3, 60),
        ('sell', 100, 'avg', .2, 30), # sell 100 if 20% above avg and don't sell till next day
        ('sell', 50, 'avg', .1, 20),
        # ('sell', 5, 'avg', .02, 5),
        # ('sell', 3, 'avg', .01, 2),

        ('sell', 2, 10, .01, 2),

        # Buy in case of recent drops
        # ('buy', 20, 60, -.01)
        # ('buy', 10, 15, -.01, 6),
        ('buy', 5, 15, -.015, 6),
        ('buy', 3, 10, -.01, 2),
        ('buy', 2, 5, -.005, 1),

        # sell in case of recent rise
        # ('sell', 50, 30, .05, 10),
        # ('sell', 100, 12 * 60, .06, 30),
        # ('sell', 50, 30*24*60, .1)

    ],
}

VISUALIZATION_WIN = 60*24*7 # show the plot for each week


def run_simulation(config):
    market = BTCMarketSimulator(
        start_timestamp=int(datetime(year=2020, month=10, day=1).timestamp()),
        end_timestamp=int(datetime(year=2020, month=12, day=30).timestamp()),
        btc_price_csv='data/bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv'
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

    # trader = WindowTrader(
    #     decision_profile=config['decision_profile'],
    #     credit=CREDIT,
    #     trade_interval=config["sleep_time"],
    #     buy_commission=BUY_COMMISSION,
    #     sell_commission=SELL_COMMISSION
    # )

    trader = LSTMTrader(
        model_path='models/lstml_2020_1_9',
        scalar_path='models/scaler.pkl',
        credit=CREDIT,
        trade_interval=60,
        buy_commission=BUY_COMMISSION,
        sell_commission=SELL_COMMISSION
    )

    simulation = MarketSimulator(market, trader, config)

    simulation.run(VISUALIZATION_WIN)
    # simulation.save_results()
    simulation.plot_all_history()

if __name__ == '__main__':
    run_simulation(CONFIG)




