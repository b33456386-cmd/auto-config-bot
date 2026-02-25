import os
import requests

TOKEN = os.getenv("8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM")
CHAT_ID = os.getenv("@jdkdjjdjkf")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    print(response.text)

def main():
    print("Bot started...")
    send_message("✅ ربات با موفقیت اجرا شد!")

if name == "main":
    main()
