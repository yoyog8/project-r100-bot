# R100MarketBot

This is the Project R-100 AI trading assistant running on Telegram via Flask + Railway.

## Setup

1. Set the following environment variables:
   - `BOT_TOKEN`
   - `TELEGRAM_ID`
   - `PORT` = 8000

2. Deploy to Railway and set webhook via:

```python
import requests
BOT_TOKEN = "your_token"
WEBHOOK_URL = "https://your-app-name.up.railway.app/webhook"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
res = requests.post(url, json={"url": WEBHOOK_URL})
print(res.text)
```
