
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

open_positions = {}

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_ID, "text": text}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message("✅ Project R-100 v3.0 已啟動（市場掃描 + 單筆追蹤模式）")
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "✅ R100MarketBot is running with BingX price logic."

def get_price(symbol):
    timestamp = str(int(time.time() * 1000))
    query = f"symbol={symbol}&timestamp={timestamp}"
    sign = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = {"X-BX-APIKEY": API_KEY}
    url = f"https://open-api.bingx.com/openApi/swap/v2/quote/price?{query}&signature={sign}"
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if data.get("code") == 0:
        return float(data["data"]["price"])
    return None

def scan_market():
    symbols = ["BTC-USDT", "ETH-USDT", "ARB-USDT", "OP-USDT"]
    while True:
        for symbol in symbols:
            price = get_price(symbol)
            if price and symbol not in open_positions:
                decision = random.choices(["進場", "觀望"], weights=[0.6, 0.4])[0]
                if decision == "進場":
                    direction = random.choice(["做多", "做空"])
                    sl = round(price * (0.985 if direction == "做多" else 1.015), 4)
                    tp = round(price * (1.015 if direction == "做多" else 0.985), 4)
                    open_positions[symbol] = {
                        "price": price,
                        "sl": sl,
                        "tp": tp,
                        "direction": direction,
                        "open_time": time.time()
                    }
                    send_message(f"【R-100 訊號】\n幣種：{symbol.replace('-', '/')}\n方向：{direction}\n進場價格：{price}\n止損價格：{sl}\n止盈目標：{tp}")
        time.sleep(300)

def track_positions():
    while True:
        now = time.time()
        for symbol in list(open_positions.keys()):
            pos = open_positions[symbol]
            price = get_price(symbol)
            if not price:
                continue

            if pos["direction"] == "做多":
                if price <= pos["sl"]:
                    send_message(f"【R-100 出場】{symbol} 已觸及止損：{price}")
                    del open_positions[symbol]
                elif price >= pos["tp"]:
                    send_message(f"【R-100 出場】{symbol} 已觸及止盈：{price}")
                    del open_positions[symbol]
                elif now - pos["open_time"] > 900:
                    send_message(f"【R-100 撤單】{symbol} 超過 15 分鐘未達目標，撤出：{price}")
                    del open_positions[symbol]
            else:
                if price >= pos["sl"]:
                    send_message(f"【R-100 出場】{symbol} 已觸及止損：{price}")
                    del open_positions[symbol]
                elif price <= pos["tp"]:
                    send_message(f"【R-100 出場】{symbol} 已觸及止盈：{price}")
                    del open_positions[symbol]
                elif now - pos["open_time"] > 900:
                    send_message(f"【R-100 撤單】{symbol} 超過 15 分鐘未達目標，撤出：{price}")
                    del open_positions[symbol]
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=scan_market, daemon=True).start()
    threading.Thread(target=track_positions, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
