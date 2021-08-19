# tick collector
📂 Collect [Binance](https://www.binance.com/kr/register?ref=19858986) Tick Data using Websocket and Automatically Store it to AWS S3.

---
## **Prerequisite**
- install docker🐳

# How to start

### **1. Set `.env` file variables**

```.env
# market type: { SPOT or FUTURE }
market=SPOT

# multiple symbols {base asset}{quote asset} (ex. BTCUSDT) w/ comma separated
symbols=BTCUSDT,ETHUSDT

# a condition indicating whenever the current file should be closed and a new one started.
# human-friendly parametrization of one of the previously enumerated types.
# ex) "1 GB", "4 days", "10h", "monthly", "18:00", "sunday", "monday at 12:00"
rotation=12:00

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


### **2. Set a schedule when you upload data to s3**

Edit `docker-compose.yaml` file, line 18  👉 [here](https://github.com/lucky7323/tick_collector/blob/24e26c3353aa86f4f67f34617e2c5313ee2f7ef2/docker-compose.yaml#L18)
```yaml
ofelia.job-exec.app.schedule: "0 0 0 * *"
```
The above default setting means that tick data is uploaded to S3 every midnight.

[Scheduling format](https://godoc.org/github.com/robfig/cron) is the same as the Go implementation of `cron`. E.g. `@every 10s` or `0 0 1 * * *` (every night at 1 AM).

**Note**: the format starts with seconds, instead of minutes.


### **3. Start collecting data!**

```sh
$ docker-compose build
$ docker-compose up -d
```

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

---
# FAQ
- [What is AWS S3 bucket?](https://aws.amazon.com/s3/?nc1=h_ls)
- [What is `aws_access_key` and `aws_secret_key`?](https://docs.aws.amazon.com/ko_kr/general/latest/gr/aws-access-keys-best-practices.html)
- [What is `telegram_token`?](https://t.me/botfather)
- [How to get `telegram_chat_id`](https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659)
- [What is `rotation`?](https://loguru.readthedocs.io/en/stable/api/logger.html#file)
