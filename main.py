import requests
import os
import time
import base64
import re

# --- تنظیمات اختصاصی ---
BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf"
MY_NAME = "jdkdjjdjkf"
HISTORY_FILE = "sent_configs.txt"

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/soroushmhm/v2ray-config-collector/main/protocols/vless",
    "https://raw.githubusercontent.com/soroushmhm/v2ray-config-collector/main/protocols/vmess",
    "https://raw.githubusercontent.com/soroushmhm/v2ray-config-collector/main/protocols/trojan",
    "https://raw.githubusercontent.com/ts-sf/v2ray-config-collector/main/sub/mix",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/result/nodes"
]

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(config_hash):
    with open(HISTORY_FILE, "a") as f:
        f.write(config_hash + "\n")

def get_info(config):
    conf_upper = config.upper()
    info = {"country": "بین‌المللی", "flag": "🌐", "hashtag": "#International"}
    
    if any(x in conf_upper for x in ["IRAN", " IR ", "|IR|", "MCI", "IRANCELL", "HAMRAH"]):
        info = {"country": "ایران", "flag": "🇮🇷", "hashtag": "#ایران #Iran"}
    elif any(x in conf_upper for x in ["GERMANY", " DE ", "|DE|"]):
        info = {"country": "آلمان", "flag": "🇩🇪", "hashtag": "#آلمان #Germany"}
    elif any(x in conf_upper for x in ["UNITED STATES", " US ", "|US|", "USA"]):
        info = {"country": "آمریکا", "flag": "🇺🇸", "hashtag": "#آمریکا #USA"}
    elif any(x in conf_upper for x in ["TURKEY", " TR ", "|TR|"]):
        info = {"country": "ترکیه", "flag": "🇹🇷", "hashtag": "#ترکیه #Turkey"}
    
    return info

def rename_config(config, new_name):
    # پاکسازی اسم قبلی و گذاشتن اسم تو
    if "#" in config:
        config = config.split("#")[0]
    return f"{config}#{new_name}"

def send_to_telegram(config):
    country_info = get_info(config)
    named_config = rename_config(config, MY_NAME)
    
    if config.startswith("vless"): proto, p_hash = "⚡️ VLESS", "#VLESS"
    elif config.startswith("vmess"): proto, p_hash = "💥 VMESS", "#VMESS"
    elif config.startswith("trojan"): proto, p_hash = "🛡 TROJAN", "#Trojan"
    else: proto, p_hash = "🚀 CONFIG", "#V2ray"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    text = (
        f"━━━━━━━━━━━━━━━\n"
        f"{proto} | {country_info['flag']} {country_info['country']}\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"`{named_config}`\n\n"
        f"✈️\n\n"
        f"✨ کـانفیگ‌های بیـشتر: {CHAT_ID} ✨\n\n"
        f"{p_hash} {country_info['hashtag']}\n"
        f"#فیلترشکن #رایگان #VPN #Free_VPN"
    )
    
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=10)

if __name__ == "__main__":
    history = get_history()
    new_count = 0
    
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=20)
            if res.status_code == 200:
                text_data = res.text
                
                # اگه دیتا Base64 بود، بازش کن
                if "://" not in text_data:
                    try:
                        text_data = base64.b64decode(text_data).decode('utf-8')
                    except: pass
                
                configs = text_data.splitlines()
                for conf in configs:
                    conf = conf.strip()
                    # فقط پروتکل های معتبر و غیرتکراری
                    if conf and conf.startswith(("vless://", "vmess://", "trojan://", "ss://")) and conf not in history:
                        send_to_telegram(conf)
                        save_history(conf)
                        new_count += 1
                        time.sleep(3) # مکث بین پیام ها
                        
                        if new_count >= 10: break
                if new_count >= 10: break
        except Exception as e:
            print(f"Error: {e}")
