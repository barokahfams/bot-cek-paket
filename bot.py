import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bs4 import BeautifulSoup

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")

def start(update, context):
    update.message.reply_text(
        "Silahkan kirim nomor XL untuk dicek.\nContoh: 08781234xxxx"
    )

def cek_nomor(update, context):
    nomor = update.message.text.strip()

    if not nomor.startswith("08"):
        update.message.reply_text("Nomor tidak valid!")
        return

    # request ke website
    url = API_URL + nomor
    response = requests.get(url)

    if response.status_code != 200:
        update.message.reply_text("Gagal mengambil data!")
        return

    # parsing HTML
    soup = BeautifulSoup(response.text, "html.parser")

    result_section = soup.find("div", class_="result")
    if not result_section:
        update.message.reply_text("Data tidak ditemukan!")
        return

    hasil = result_section.get_text("\n", strip=True)
    update.message.reply_text(f"📊 *Hasil cek {nomor}:*\n\n{hasil}", parse_mode="Markdown")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, cek_nomor))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
