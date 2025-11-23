import os
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bs4 import BeautifulSoup

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")

def start(update, context):
    update.message.reply_text(
        "Masukkan nomor XL untuk dicek.\nContoh: 0878xxxx"
    )

def cek_nomor(update, context):
    nomor = update.message.text.strip()

    if not nomor.startswith("08"):
        update.message.reply_text("Nomor tidak valid!")
        return

    url = API_URL + nomor

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        hasil = soup.get_text("\n", strip=True)
        update.message.reply_text(hasil)

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, cek_nomor))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
