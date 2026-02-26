import requests
import os

BOT_TOKEN = os.getenv("8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM")
CHAT_ID = os.getenv("@jdkdjjdjkf")

def main():
    text = "ربات تست شد ✅"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=data)

if name == "main":
    main()
