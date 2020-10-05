from binance.client import Client
from binance.websockets import BinanceSocketManager
import argparse
import logging.handlers

file_name = "ticker.csv"
logger = logging.getLogger('tick')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=10**9, backupCount=20)
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def process_message(msg):
    msg = f"{msg['e']},{msg['E']},{msg['s']},{msg['t']},{msg['p']},{msg['q']},{msg['b']},{msg['a']},{msg['T']},{msg['m']}"
    logger.info(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, type=str, help="symbol {base asset}{quote asset} (ex. 'BTCUSDT')")
    symbol = parser.parse_args().symbol.upper()
    client = Client("", "")
    bm = BinanceSocketManager(client)
    conn_key = bm.start_trade_socket(symbol, process_message)
    bm.start()
    print(f'Started Collecting Tick Data of {symbol}...')

