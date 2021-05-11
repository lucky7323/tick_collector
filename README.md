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
- Set `config.json`
- Example
```json
{
  "AWS_ACCESS_KEY": "",
  "AWS_SECRET_KEY": "",
  "S3_BUCKET": "",
  "S3_BUCKET_PATH": "tickdata/",
  "TELEGRAM_TOKEN": "",
  "TELEGRAM_CHAT_ID": ""
}
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

**3. Run Collector with the Symbol**
```sh
$ python3 collector.py --symbol BTCUSDT
```
- Recommend running in the background. Ex) [Screen](https://linuxize.com/post/how-to-use-linux-screen/), [nohup](https://en.wikipedia.org/wiki/Nohup)

---
# Note
- Tick data is stored in the form of csv.

```javascript
// This is One Single Tick Data from Binance Websocket
{
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order ID
  "a": 50,          // Seller order ID
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}
```

```javascript
// This is .csv file
"trade",123456789,"BNBBTC",12345,"0.001","100",88,50,123456785,true
"trade",123456922,"BNBBTC",12346,"0.001","100",88,50,123456805,true
...
```

- Trade ID must increase by 1.
- The maximum size of a .csv file is 1GB, and It automatically rolls over to new files and be compressed.
You can modify setting values *in `collector.py` 10 lines*

```python
logger.add(f"{data_dir}{prefix}{ticker}" + "_{time}.csv", format="{message}", rotation="1 GB", compression="zip",
```

- If you proceed with step 2-3, the collected tick-data is automatically sent to configured s3 bucket at midnight every day.
- You can modify setting values in `add_cron.sh`

---
# Update
### (21.05.11) Support future market data
- Future market aggregate trade data is also stored in the form of csv.
```javascript
// This is Aggregate Trade Data of Future Market from Binance Websocket
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

