import requests

BOT_TOKEN = "bot7955074053:AAEBG7JdRelVR5vOzVrBOIcYFRLXk-d410c"
WEBHOOK_URL = "https://web-production-0883b.up.railway.app/webhook"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": WEBHOOK_URL}
res = requests.post(url, json=payload)
print(res.text)
