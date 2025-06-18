import logging
from flask import Flask
from threading import Thread
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID

# Настройка логгера 
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

# Телеграм API
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'
client = TelegramClient('sticker_filter_session', api_id, api_hash)

# Цель
target_username = 'Sleep_paralycis'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

# Flask-заглушка для Render
app = Flask(__name__)

@app.route('/')
def index():
    return '🟢 Telegram Sticker Remover is running!'

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Обработка сообщений
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
                        logger.info(f"❌ Удалён стикер от @{target_username} из приватного пака.")
                        return  # не продолжаем дальше

# Запуск
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    Thread(target=run_flask).start()

    # Запускаем Telethon
    async def main():
        await client.start()
        logger.info("✅ Бот запущен и слушает новые сообщения...")
        await client.run_until_disconnected()

    asyncio.run(main())
