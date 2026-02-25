import requests
import time

# اطلاعاتی که دادی
BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf"

# لیست منابع (می‌تونی منابع بیشتری اضافه کنی)
SOURCES = [
    "https://raw.githubusercontent.com/IranianCypherpunks/sub/main/config",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_configs():
    all_configs = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                # جدا کردن خط‌ها و برداشتن ۵ تای اول برای تست
                lines = res.text.splitlines()
                all_configs.extend(lines[:3]) 
        except:
            print(f"Error fetching from {url}")
    return all_configs

def send_to_telegram(config):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🚀 New Config Found:\n\n`{config}`",
        "parse_mode": "MarkdownV2"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    configs = get_configs()
    for conf in configs:
        if conf.strip(): # اگر خط خالی نبود
            send_to_telegram(conf)
            time.sleep(2) # برای اینکه تلگرام اسپم تشخیص نده
