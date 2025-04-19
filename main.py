from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook received:", data)  # Debug：印出 webhook 資料

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        print("Message text:", text)  # Debug：印出訊息內容

        if text == "/start":
            send_message(chat_id, "✅ Project R-100 已啟動！我會自動每 5 分鐘掃描市場，當有重大波動、潛在訊號或進場條件成立時會即時通知你。")
    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    print("Sending message:", payload)  # Debug：印出發送內容
    res = requests.post(url, json=payload)
    print("Telegram response:", res.status_code, res.text)  # Debug：印出 Telegram 回應

@app.route("/", methods=["GET"])
def index():
    return "✅ R100MarketBot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
