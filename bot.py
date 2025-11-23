import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bs4 import BeautifulSoup

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")

async def start(update, context):
    await update.message.reply_text(
        "Masukkan nomor XL untuk dicek.\nContoh: 0878xxxx"
    )

async def cek_nomor(update, context):
    nomor = update.message.text.strip()

    if not nomor.startswith("08"):
        await update.message.reply_text("Nomor tidak valid!")
        return

    url = API_URL + nomor

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        hasil = soup.get_text("\n", strip=True)
        await update.message.reply_text(hasil)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cek_nomor))

    app.run_polling()

if __name__ == "__main__":
    main()
