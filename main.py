import os
import asyncio
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_name = "session"  # или путь к .session

app = Flask(__name__)

# Flask "затычка", чтобы Render не ругался
@app.route('/')
def home():
    return 'Bot is alive!'

# Запускаем Flask-сервер в отдельном потоке
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()

# Телеграм-клиент
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage)
async def handle(event):
    sender = await event.get_sender()
    print(f"Сообщение от {sender.username}: {event.text}")
    await event.reply("Принято!")

async def main():
    await client.start()
    print("Бот запущен и ждет сообщений...")
    await client.run_until_disconnected()

# Запускаем event loop
asyncio.run(main())
