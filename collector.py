from binance.client import Client
from binance.websockets import BinanceSocketManager
import argparse
from loguru import logger


def set_logger(log_dir, ticker):
    logger.remove()
    logger.add(f"{log_dir}{ticker}" + "_{time}.csv", format="{message}", rotation="2 GB", compression="zip")


def process_message(msg):
    msg = f"{msg['e']},{msg['E']},{msg['s']},{msg['t']},{msg['p']},{msg['q']},{msg['b']},{msg['a']},{msg['T']},{msg['m']}"
    logger.info(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, type=str, help="symbol {base asset}{quote asset} (ex. 'BTCUSDT')")
    parser.add_argument("--log_dir", type=str, help="log directory path", default="./logs/")
    args = parser.parse_args()
    symbol = args.symbol.upper()

    set_logger(args.log_dir, symbol)
    client = Client("", "")
    bm = BinanceSocketManager(client)
    conn_key = bm.start_trade_socket(symbol, process_message)
    bm.start()
    print(f'Started Collecting Tick Data of {symbol}...')

