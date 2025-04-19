# R100MarketBot

Project R-100 是一個基於 Telegram Bot 與 AI 分析的市場監控機器人，部署於 Railway 平台。

---

## 部署需求

- Python 3.10+
- Flask
- pyTelegramBotAPI

---

## 安裝依賴

```
pip install -r requirements.txt
```

---

## 設定環境變數

請在 Railway 或本地設定以下變數：

```
BOT_TOKEN=你的 Telegram Bot Token
TELEGRAM_ID=你的 Telegram ID（選填）
PORT=8000
```

---

## 啟動方式

若於本地啟動：

```
python main.py
```

---

## 設定 Telegram Webhook

部署成功後，請於本地或 Replit 執行 `set_webhook.py`：

```python
import requests

BOT_TOKEN = "your_bot_token"
WEBHOOK_URL = "https://your-railway-app.up.railway.app/webhook"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": WEBHOOK_URL}
res = requests.post(url, json=payload)
print(res.text)
```

---

## Bot 功能

目前支援 `/start` 指令，未來將整合自動掃描市場、AI 分析與即時回報機制。
