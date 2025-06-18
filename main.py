from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID
from flask import Flask
from threading import Thread
import asyncio

# Прямые ключи Telegram API
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'

# Название сессии — создаст файл sticker_filter.session
client = TelegramClient('sticker_filter', api_id, api_hash)

# Цель — кто отправляет и ID стикерпака
target_username = 'Sleep_paralycis'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

# Flask-заглушка для Render (обманка, чтоб не вырубало)
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Обработчик входящих сообщений
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
                        print(f"Удалён стикер из приватного пака от @{target_username}")

# Основной запуск
async def main():
    await client.start()
    print("Скрипт запущен. Жду стикер от цели...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(main())
