from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID

# Telegram API параметры
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'

# Инициализация Telegram клиента
client = TelegramClient('sticker_filter', api_id, api_hash)

# Настройки фильтра
target_username = 'Armoredb_user'
target_pack_id = 4798983069690233625
target_access_hash = -4231871290391784105

# Flask-приложение (обманка)
app = Flask(__name__)

@app.route('/')
def home():
    return 'OK', 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)  # Render ожидает открытый порт

# Обработка входящих сообщений
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
                        print(f"Удалён стикер от @{target_username}")

# Запуск
if __name__ == '__main__':
    Thread(target=run_flask).start()  # Flask в фоне
    client.start()
    print("Бот запущен и слушает события...")
    client.run_until_disconnected()

