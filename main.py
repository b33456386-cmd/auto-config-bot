import requests
import os
import time
import base64

# --- تنظیمات اختصاصی ---
BOT_TOKEN = "8551688721:AAHyFlOL5WZYjgAuswz81X_SCi898k1DOUM"
CHAT_ID = "@jdkdjjdjkf"
MY_NAME = "jdkdjjdjkf"
HISTORY_FILE = "sent_configs.txt"

# منابع کامل برای همه پروتکل‌ها
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
    
    # تشخیص کشور و تنظیم هشتگ اختصاصی
    if any(x in conf_upper for x in ["IRAN", " IR ", "|IR|", "MCI", "IRANCELL", "HAMRAH"]):
        info = {"country": "ایران", "flag": "🇮🇷", "hashtag": "#ایران #Iran"}
    elif any(x in conf_upper for x in ["GERMANY", " DE ", "|DE|"]):
        info = {"country": "آلمان", "flag": "🇩🇪", "hashtag": "#آلمان #Germany"}
    elif any(x in conf_upper for x in ["UNITED STATES", " US ", "|US|", "USA"]):
        info = {"country": "آمریکا", "flag": "🇺🇸", "hashtag": "#آمریکا #USA"}
    elif any(x in conf_upper for x in ["TURKEY", " TR ", "|TR|"]):
        info = {"country": "ترکیه", "flag": "🇹🇷", "hashtag": "#ترکیه #Turkey"}
    elif any(x in conf_upper for x in ["FINLAND", " FI ", "|FI|"]):
        info = {"country": "فنلاند", "flag": "🇫🇮", "hashtag": "#فنلاند #Finland"}
    
    return info

def rename_config(config, new_name):
    if "#" in config:
        base_part = config.split("#")[0]
        return f"{base_part}#{new_name}"
    return f"{config}#{new_name}"

def send_to_telegram(config):
    country_info = get_info(config)
    named_config = rename_config(config, MY_NAME)
    
    # تعیین پروتکل و هشتگ مربوطه
    if config.startswith("vless"):
        proto, p_hash = "⚡️ VLESS", "#VLESS"
    elif config.startswith("vmess"):
        proto, p_hash = "💥 VMESS", "#VMESS"
    elif config.startswith("trojan"):
        proto, p_hash = "🛡 TROJAN", "#Trojan"
    else:
        proto, p_hash = "🚀 CONFIG", "#V2ray"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # چیدمان با هشتگ‌های پربازدید برای بالا رفتن آمار
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
                        time.sleep(4) # کمی مکث بیشتر برای امنیت
                        if new_count >= 15: break
                if new_count >= 15: break
        except: continue
