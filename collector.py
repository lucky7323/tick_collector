from binance.client import Client
from binance.websockets import BinanceSocketManager
import argparse
from loguru import logger


def set_logger(data_dir, ticker):
    logger.remove()
    logger.add(f"{data_dir}{ticker}" + "_{time}.csv", format="{message}", rotation="2 GB", compression="zip",
               filter=lambda record: record["extra"]["task"] == "data")


def process_message(msg):
    msg = f"{msg['e']},{msg['E']},{msg['s']},{msg['t']},{msg['p']},{msg['q']},{msg['b']},{msg['a']},{msg['T']},{msg['m']}"
    data_logger = logger.bind(task="data")
    data_logger.info(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, type=str, help="symbol {base asset}{quote asset} (ex. 'BTCUSDT')")
    parser.add_argument("--data_dir", type=str, help="data directory path", default="./data/")
    args = parser.parse_args()
    symbol = args.symbol.upper()

    set_logger(args.data_dir, symbol)
    client = Client("", "")
    bm = BinanceSocketManager(client)
    conn_key = bm.start_trade_socket(symbol, process_message)
    bm.start()
    print(f'Started Collecting Tick Data of {symbol}...')

