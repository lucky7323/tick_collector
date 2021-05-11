from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
import asyncio
import argparse
from loguru import logger


def set_logger(data_dir, ticker, future: bool):
    prefix = "future_" if future else ""
    logger.remove()
    logger.add(f"{data_dir}{prefix}{ticker}" + "_{time}.csv", format="{message}", rotation="1 GB", compression="zip",
               filter=lambda record: record["extra"]["task"] == "data")


def process_message(msg, future: bool):
    if future:
        msg = f"{msg['e']},{msg['E']},{msg['s']},{msg['a']},{msg['p']},{msg['q']},{msg['f']},{msg['l']},{msg['T']},{msg['m']}"
    else:
        msg = f"{msg['e']},{msg['E']},{msg['s']},{msg['t']},{msg['p']},{msg['q']},{msg['b']},{msg['a']},{msg['T']},{msg['m']}"
    data_logger = logger.bind(task="data")
    data_logger.info(msg)


async def main(symbol: str, future: bool):
    market_type = "future" if future else "spot"
    print(f'Started Collecting Tick Data of {symbol}...({market_type} market)')
    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client)

    if future:
        async with bsm.aggtrade_futures_socket(symbol) as socket:
            while True:
                res = await socket.recv()
                process_message(res['data'], future)
    else:
        async with bsm.trade_socket(symbol) as socket:
            while True:
                res = await socket.recv()
                process_message(res, future)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, type=str, help="symbol {base asset}{quote asset} (ex. 'BTCUSDT')")
    parser.add_argument("--data_dir", type=str, help="data directory path", default="./data/")
    parser.add_argument("--future", action='store_true', help="for future market data")
    args = parser.parse_args()
    symbol = args.symbol.upper()

    set_logger(args.data_dir, symbol, args.future)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(symbol, args.future))

