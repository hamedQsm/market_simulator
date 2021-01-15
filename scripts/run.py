from datetime import datetime

from market_trading.market_simulator import MarketSimulator
from market_trading.markets.BTCMarketSimulator import BTCMarketSimulator
from market_trading.traders.SimpleTrader import SimpleTrader

CREDIT = 10000
BUY_COMMISSION = .01
SELL_COMMISSION = .01

sleep_time = 60 * 1
initial_buy = .2
avg_price_down_step = .99
profit_margin = .5

def run_simulation():
    market = BTCMarketSimulator(
        int(datetime(year=2020, month=1, day=1).timestamp()),
        '../data/bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv'
    )

    trader = SimpleTrader(
        initial_buy_prcnt=initial_buy,
        avg_price_down_step=avg_price_down_step,
        profit_margin=profit_margin,
        credit=CREDIT,
        trade_interval=sleep_time,
        buy_commission=BUY_COMMISSION,
        sell_commission=SELL_COMMISSION
    )

    simulation = MarketSimulator(market, trader)

    simulation.run()

    simulation.plot_history()

if __name__ == '__main__':
    run_simulation()




