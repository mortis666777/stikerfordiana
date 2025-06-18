from flask import Flask
from threading import Thread
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID

# Session file must be present
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'

session_name = 'armored_user_session'  # Name of your saved .session file

target_username = 'Armoredb_user'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

client = TelegramClient(session_name, api_id, api_hash)

# Flask dummy
app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот запущен и слушает события!'

# Телеграм обработчик
@client.on(events.NewMessage(incoming=True))
async def handle(event):
    sender = await event.get_sender()
    if sender.username == target_username and event.sticker:
        for attr in event.document.attributes:
            if isinstance(attr, DocumentAttributeSticker):
                sticker_set = attr.stickerset
                if isinstance(sticker_set, InputStickerSetID):
                    if sticker_set.id == target_pack_id and sticker_set.access_hash == target_access_hash:
                        await event.delete()
                        print(f"✅ Удалён стикер от @{target_username}")

# Асинхронный запуск клиента
async def start_client():
    await client.start()
    print("📡 Телеграм клиент запущен...")
    await client.run_until_disconnected()

# Запускаем телеграм бота в отдельном потоке
def run_telethon():
    asyncio.run(start_client())

# Запускаем Flask
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Основной запуск
if __name__ == '__main__':
    # Стартуем Telethon в фоновом потоке
    Thread(target=run_telethon).start()
    # Запускаем Flask-сервер
    run_flask()
