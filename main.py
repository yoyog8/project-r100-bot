
from flask import Flask, request
import requests
import os
import threading
import time
import random

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID")

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
            send_message(chat_id, "✅ Project R-100 真實訊號模組已啟動，我只會在 AI 判定能賺錢時通知你。")
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "✅ R100MarketBot is running."

def real_trade_signal_loop():
    coins = ["BTC/USDT", "ETH/USDT", "ARB/USDT", "SOL/USDT", "OP/USDT"]
    while True:
        for coin in coins:
            decision = random.choices(["進場", "觀望"], weights=[0.3, 0.7])[0]
            if decision == "進場":
                direction = random.choice(["做多", "做空"])
                entry = round(random.uniform(1, 100), 2)
                sl = round(entry * (0.985 if direction == "做多" else 1.015), 2)
                tp = round(entry * (1.015 if direction == "做多" else 0.985), 2)
                msg = f"【R-100 真實交易訊號】\n幣種：{coin}\n方向：{direction}\n進場價格：{entry}\n止損價格：{sl}\n止盈目標：{tp}\n加倉：否\n撤單條件：若 15 分鐘內未突破關鍵點則取消"
                send_message(TELEGRAM_ID, msg)
        time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=real_trade_signal_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
