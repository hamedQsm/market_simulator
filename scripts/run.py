from datetime import datetime

from market_trading.market_simulator import MarketSimulator
from market_trading.markets.BTCMarketSimulator import BTCMarketSimulator
from market_trading.traders.simple_traders import AVGTrader, WindowTrader

CREDIT = 1000
BUY_COMMISSION = .01
SELL_COMMISSION = .01

sleep_time = 60 * 5
initial_buy = 10
sell_step = 10
loss_margin = .01
profit_margin = .02
loss_aversion_margin = .5  # sell if you are more than this in loss

sell_win_size = 10
buy_win_size = 10

def run_simulation():
    market = BTCMarketSimulator(
        start_timestamp=int(datetime(year=2017, month=6, day=1).timestamp()),
        end_timestamp=int(datetime(year=2019, month=1, day=1).timestamp()),
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
        sell_win_size=sell_win_size,
        buy_win_size=buy_win_size,
        initial_buy_step=initial_buy,
        sell_step=sell_step,
        loss_margin=loss_margin,
        profit_margin=profit_margin,
        loss_aversion_margin=loss_aversion_margin,
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




