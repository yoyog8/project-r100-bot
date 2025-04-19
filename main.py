from flask import Flask, request
import telebot
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content-type', 403

@app.route('/', methods=['GET'])
def index():
    return "R100MarketBot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ Project R-100 已啟動！我會自動每 5 分鐘掃描市場，當有重大波動、潛在訊號或進場條件成立時會即時通知你。")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))