import requests
import os
import time
import base64
import urllib.parse

# --- تنظیمات اختصاصی تو ---
BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf"
MY_NAME = "jdkdjjdjkf" # اسمی که ته کانفیگ‌ها میفته
HISTORY_FILE = "sent_configs.txt"

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/soroushmhm/v2ray-config-collector/main/protocols/vless",
    "https://raw.githubusercontent.com/ts-sf/v2ray-config-collector/main/sub/mix",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/result/nodes"
]

def rename_config(config, new_name):
    try:
        # این بخش اسم کانفیگ رو بعد از هشتگ (#) عوض می‌کنه
        if "#" in config:
            base_part = config.split("#")[0]
            return f"{base_part}#{new_name}"
        else:
            return f"{config}#{new_name}"
    except:
        return config

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(config_hash):
    with open(HISTORY_FILE, "a") as f:
        f.write(config_hash + "\n")

def send_to_telegram(config):
    # تغییر اسم کانفیگ به اسم کانال تو
    named_config = rename_config(config, MY_NAME)
    
    if config.startswith("vless"): title = "⚡️ کانفیگ ویژه‌ی VLESS"
    elif config.startswith("vmess"): title = "💥 کانفیگ جدید VMESS"
    elif config.startswith("trojan"): title = "🛡 کانفیگ اختصاصی TROJAN"
    else: title = "🚀 کانفیگ جدید سیستم"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    text = (
        f"{title}\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"`{named_config}`\n\n"
        f"✈️\n\n"
        f"✨ کـانفیگ‌های بیـشتر: {CHAT_ID} ✨\n"
        f"⭐️ به دوستات هم بفرست ⭐️"
    )
    
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except: pass

if __name__ == "__main__":
    history = get_history()
    new_count = 0
    
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                content = res.text
                if not any(x in content[:50] for x in ["vless", "vmess", "ss", "trojan"]):
                    try: content = base64.b64decode(content).decode('utf-8')
                    except: pass
                
                configs = content.splitlines()
                for conf in configs:
                    conf = conf.strip()
                    if conf and conf not in history and conf.startswith(("vless", "vmess", "trojan", "ss")):
                        send_to_telegram(conf)
                        save_history(conf)
                        new_count += 1
                        time.sleep(3)
                        if new_count >= 10: break
                if new_count >= 10: break
        except: continue
