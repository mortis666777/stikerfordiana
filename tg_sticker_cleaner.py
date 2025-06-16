from telethon import TelegramClient, events

# Вставь свои значения
api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'

client = TelegramClient('sticker_filter', api_id, api_hash)

# Цель — юзер @Armoredb_user
target_username = 'Armoredb_user'
target_emoji = '😡'

@client.on(events.NewMessage(incoming=True))
async def handle(event):
    sender = await event.get_sender()

    # Проверка: от нужного пользователя и сообщение — стикер
    if sender.username == target_username and event.sticker:
        # Проверка на нужное emoji
        if event.file.emoji == target_emoji:
            await event.delete()
            print(f'Удалён стикер с эмоджи {target_emoji} от @{target_username}')
            # Если хочешь, добавь ответ:
            # await event.respond("Удалён стикер с эмоджи 😡.")

client.start()
print("Скрипт запущен. Ожидаем сообщения...")
client.run_until_disconnected()
