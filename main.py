import os
import time
import requests
from telegram import Bot

# گرفتن توکن ربات تلگرام و URL API
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
CHAT_ID = os.getenv("CHAT_ID")  # آی‌دی چت برای ارسال پیام
API_URL = os.getenv("API_URL")  # آدرس API برای چک کردن توکن‌های جدید

def fetch_new_tokens():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching tokens: {e}")
        return None

def send_token_info(token_info):
    message = f"""🚀 توکن جدید پیدا شد!
اسم: {token_info['name']} ({token_info['symbol']})
قیمت: ${token_info['price']}
رشد: {token_info['growth']}%
لیکوییدیتی: {token_info['liquidity']}$
FDV: {token_info['fdv']}$
ATH: {token_info['ath']}$
تغییر: {token_info['ath_change']}%
وضعیت امنیتی: {"✅ امن" if token_info['is_safe'] else "❌ مالکیت واگذار نشده"}
لاک LP: {"✅ بله" if token_info['lp_locked'] else "❌ خیر"}
مالیات خرید: {token_info['buy_tax']}% | فروش: {token_info['sell_tax']}%
Dev Holdings: {token_info['dev_holdings']}%
"""
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    sent_tokens = set()
    while True:
        tokens = fetch_new_tokens()
        if tokens:
            for token in tokens:
                if token['address'] not in sent_tokens:
                    send_token_info(token)
                    sent_tokens.add(token['address'])
        time.sleep(60)

if __name__ == "__main__":
    main()
