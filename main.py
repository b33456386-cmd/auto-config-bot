import requests

BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    print(response.text)

def main():
    send_message("🔥 ربات با موفقیت کار کرد!")

if name == "main":
    main()
