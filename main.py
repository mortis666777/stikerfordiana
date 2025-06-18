from flask import Flask
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID
import asyncio
from threading import Thread

# === Telegram Auth ===
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'
session_name = 'armored_user_session'

# === Цели ===
target_username = 'Armoredb_user'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

# === Flask App ===
app = Flask(__name__)

@app.route('/')
def home():
    return '🟢 Сервис работает'

# === Telethon Клиент ===
client = TelegramClient(session_name, api_id, api_hash)

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
                        print(f'🗑 Стикер удалён от @{target_username}')

async def start_telethon():
    print("🚀 Подключаюсь к Telegram...")
    await client.start()
    print("✅ Подключено к Telegram. Бот слушает сообщения...")
    await client.run_until_disconnected()

def run_telethon():
    asyncio.run(start_telethon())

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run_telethon).start()
    run_flask()
