# tick collector
📂 Collect [Binance](https://www.binance.com/kr/register?ref=19858986) Tick Data using Websocket

---
## How to start
**1. Install Requirements**
```
pip install -r requirements.txt
```

**2. Run collector with the symbol**
```
python collector.py --symbol "BTCUSDT"
```

---
## Note
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
- The maximum size of a .csv file is 1GB, and It automatically rolls over to 20 new files. (i.e. total 20GB) 
You can modify setting values *in `collector.py` 9 lines*

```python
handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=10**9, backupCount=20)
```
