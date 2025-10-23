import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8496126499:AAG9tbOqLRlO8fYejC3rfcSY24SZ4-MYknA"

VIDEOS = [
    "https://www.youtube.com/watch?v=Z1W-ZeszTMw",
    "https://www.youtube.com/watch?v=JwEbnUPP0ik&t=220s",
    "https://www.youtube.com/watch?v=FUJeG5BQoHA"
]

group_ids = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        group_ids.add(chat.id)
        print(f"Guruh qo‘shildi: {chat.title} (ID: {chat.id})")
    await update.message.reply_text(
        "Salom! Bot ishga tushdi. Siz qo‘shgan guruhlarga avtomatik video yuboriladi."
    )

async def send_video_task(app):
    while True:
        if group_ids:
            video = random.choice(VIDEOS)
            for gid in group_ids:
                try:
                    await app.bot.send_message(chat_id=gid, text=f"📹 Video: {video}")
                    print(f"Video yuborildi: {gid} → {video}")
                except Exception as e:
                    print(f"Xatolik {gid} ga yuborishda: {e}")
        else:
            print("Hozircha guruh yo'q.")
        await asyncio.sleep(50)  # TEST uchun 5 soniya

# --- YANGI QISMI --- #
async def main_async():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Video yuborish vazifasi
    asyncio.create_task(send_video_task(app))

    # Bot polling
    await app.initialize()
    await app.start()
    print("🤖 Bot ishga tushdi! /start buyrug‘ini yuboring.")
    await app.updater.start_polling()  # eski `run_polling` o‘rniga
    await asyncio.Event().wait()  # botni doimiy ishga tushurish

# Windows PowerShell uchun oddiy ishga tushirish
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main_async())

