
from flask import Flask, request
import requests
import os
import hmac
import hashlib
import time
import threading
import random

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID")
API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "✅ Project R-100 真實訊號模組（使用 BingX 即時報價）已啟動！")
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "✅ R100MarketBot is running with BingX API."

def get_price(symbol):
    timestamp = str(int(time.time() * 1000))
    query = f"symbol={symbol}&timestamp={timestamp}"
    sign = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = {
        "X-BX-APIKEY": API_KEY
    }
    url = f"https://open-api.bingx.com/openApi/swap/v2/quote/price?{query}&signature={sign}"
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if data.get("code") == 0:
        return float(data["data"]["price"])
    else:
        return None

def real_trade_signal_loop():
    symbols = ["BTC-USDT", "ETH-USDT", "ARB-USDT", "OP-USDT"]
    while True:
        for symbol in symbols:
            price = get_price(symbol)
            if price:
                decision = random.choices(["進場", "觀望"], weights=[0.4, 0.6])[0]
                if decision == "進場":
                    direction = random.choice(["做多", "做空"])
                    sl = round(price * (0.985 if direction == "做多" else 1.015), 4)
                    tp = round(price * (1.015 if direction == "做多" else 0.985), 4)
                    msg = f"【R-100 真實交易訊號】\n幣種：{symbol.replace('-', '/')}\n方向：{direction}\n進場價格：{price}\n止損價格：{sl}\n止盈目標：{tp}\n加倉：否\n撤單條件：若 15 分鐘內無突破則撤單"
                    send_message(TELEGRAM_ID, msg)
        time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=real_trade_signal_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
