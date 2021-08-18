# tick collector
📂 Collect [Binance](https://www.binance.com/kr/register?ref=19858986) Tick Data using Websocket and Automatically Store it to AWS S3.

---
# **Environment**
- python3.6+
- ubuntu

# How to start

**1. Install Requirements**
```sh
$ pip3 install -r requirements.txt
```

**2. Set Configuration**
- Set `.env`
- Example
```.env
# market: { SPOT or FUTURE }
market=SPOT

# multiple symbols {base asset}{quote asset} (ex. BTCUSDT) w/ comma separated
symbols=BTCUSDT,ETHUSDT

# maximum single data file size (ex. 1GB)
max_size=1 GB

# aws s3 settings
use_s3=false
aws_access_key=YOUR_AWS_ACCESS_KEY
aws_secret_key=YOUR_AWS_SECRET_KEY
s3_bucket=YOUR_S3_BUCKET_NAME
s3_bucket_path=data/

# telegram settings
use_telegram=false
telegram_token=YOUR_TELEGRAM_BOT_TOKEN
telegram_chat_id=YOUR_TELEGRAM_CHAT_ID
```
- AWS acess key & secret key: https://docs.aws.amazon.com/ko_kr/general/latest/gr/aws-access-keys-best-practices.html
- AWS S3: https://aws.amazon.com/s3/?nc1=h_ls
- Telegram token: https://t.me/botfather
- How to get telegram chat id: https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659

**3. Add Cron-job for Uploading to AWS S3**
```sh
$ sh add_cron.sh
$ service cron restart
$ crontab -l
$ service cron status
```

**4. Run Collector**
```sh
$ python3 collector.py
```
- Recommend running in the background. Ex) [Screen](https://linuxize.com/post/how-to-use-linux-screen/), [nohup](https://en.wikipedia.org/wiki/Nohup)

---
# Note
- Tick data is stored in the form of csv.

```javascript
// The Aggregate Trade Streams push trade information that is aggregated for a single taker order.
{
    "e": "aggTrade",  // Event type
    "E": 123456789,   // Event time
    "s": "BTCUSDT",   // Symbol
    "a": 5933014,     // Aggregate trade ID
    "p": "0.001",     // Price
    "q": "100",       // Quantity
    "f": 100,         // First trade ID
    "l": 105,         // Last trade ID
    "T": 123456785,   // Trade time
    "m": true,        // Is the buyer the market maker?
}
```

```javascript
// This is .csv file
aggTrade,1620744948060,BTCUSDT,476905218,55845.13,1.887,777675070,777675082,1620744948055,True
aggTrade,1620744948060,BTCUSDT,476905219,55844.48,0.191,777675083,777675083,1620744948055,True
...
```

- Binance docs for aggregate trade streams: [Link](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#aggregate-trade-streams)
- The maximum size of a .csv file is 1GB, and It automatically rolls over to new files and be compressed.
You can modify setting values `max_size` in *.env*
- If you proceed with step 2-3, the collected tick-data is automatically sent to configured s3 bucket at midnight every day.
- You can modify setting values in `add_cron.sh`

