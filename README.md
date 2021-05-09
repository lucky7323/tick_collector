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

**2. AWS S3 Configuration**
- Set `config.json`
- Example
```json
{
  "AWS_ACCESS_KEY": "",
  "AWS_SECRET_KEY": "",
  "S3_BUCKET": "",
  "S3_BUCKET_PATH": "tickdata/"
}
```

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
- The maximum size of a .csv file is 2GB, and It automatically rolls over to new files and be compressed.
You can modify setting values *in `collector.py` 9 lines*

```python
logger.add(f"{log_dir}{ticker}" + "_{time}.csv", format="{message}", rotation="2 GB", compression="zip")
```

- If you proceed with step 2-3, the collected tick-data is automatically sent to configured s3 bucket at midnight every day.
- You can modify setting values in `add_cron.sh`
