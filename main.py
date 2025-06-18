from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID
from flask import Flask
from threading import Thread
import asyncio

# === Telegram API credentials ===
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'

# Название сессии (создастся файл sticker_cleaner.session)
client = TelegramClient('sticker_cleaner', api_id, api_hash)

# === Настройки таргета ===
target_username = 'Armoredb_user'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

# === Flask сервер — для Render ===
app = Flask(__name__)

@app.route('/')
def index():
    return "Telegram Sticker Cleaner is running."

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# === Логика удаления стикеров ===
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
                        print(f"[LOG] Удалён стикер от @{target_username} из таргет-пака.")

# === Основная точка входа ===
async def main():
    await client.start()
    print("🟢 Бот запущен и слушает события...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(main())
