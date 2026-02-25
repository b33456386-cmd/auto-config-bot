import requests

# 🔑 تنظیمات
BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf"

# 📤 ارسال پیام
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    print(response.text)

# 🚀 اجرای اصلی
def main():
    send_message("🔥 ربات با موفقیت وصل شد و داره کار می‌کنه!")

if name == "main":
    main()
