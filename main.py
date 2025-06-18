from flask import Flask
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID
import asyncio
import threading

# Flask-приложение
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bot is running..."

# Telegram конфигурация
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'
session_name = 'armored_user_session'

client = TelegramClient(session_name, api_id, api_hash)

# Целевой пользователь и стикерпак
target_username = 'Armoredb_user'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

@client.on(events.NewMessage(incoming=True))
async def handle(event):
    sender = await event.get_sender()
    if sender.username == target_username and event.sticker:
        for attr in event.document.attributes:
            if isinstance(attr, DocumentAttributeSticker):
                sticker_set = attr.stickerset
                if isinstance(sticker_set, InputStickerSetID):
                    if (sticker_set.id == target_pack_id and 
                        sticker_set.access_hash == target_access_hash):
                        await event.delete()
                        print(f"❌ Стикер от @{target_username} удалён")

# Асинхронная функция для запуска Flask в фоновом потоке
def start_flask():
    app.run(host="0.0.0.0", port=8080)

# Основной запуск
async def main():
    threading.Thread(target=start_flask).start()
    await client.start()
    print("🤖 Бот запущен и слушает события...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
