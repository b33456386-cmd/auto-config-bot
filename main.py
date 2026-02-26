import requests
import os
import time
import base64

# --- تنظیمات ---
BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf" # اگه آیدی عددی گرفتی، حتما جایگزین کن

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"
]

def check_bot():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        res = requests.get(url)
        print(f"DEBUG: Bot Status -> {res.json()}")
    except Exception as e:
        print(f"DEBUG: Connection Error -> {e}")

def send_to_telegram(config):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    text = f"🚀 **تست نهایی:**\n\n`{config}#jdkdjjdjkf`"
    try:
        res = requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
        print(f"DEBUG: Telegram Response -> {res.json()}")
    except Exception as e:
        print(f"DEBUG: Send Error -> {e}")

if __name__ == "__main__":
    print("--- STARTING SCRIPT ---")
    check_bot()
    
    for url in SOURCES:
        print(f"DEBUG: Fetching URL -> {url}")
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                data = res.text
                if "://" not in data:
                    try: data = base64.b64decode(data).decode('utf-8')
                    except: pass
                
                configs = data.splitlines()
                sent_in_this_run = 0
                for conf in configs:
                    if conf.strip().startswith(("vless", "vmess")):
                        send_to_telegram(conf.strip())
                        sent_in_this_run += 1
                        time.sleep(2)
                        if sent_in_this_run >= 2: break
                print(f"DEBUG: Sent {sent_in_this_run} configs from this source.")
            else:
                print(f"DEBUG: Source Error -> Status {res.status_code}")
        except Exception as e:
            print(f"DEBUG: Loop Error -> {e}")
