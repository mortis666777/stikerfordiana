# main.py
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID

api_id = 22785739
api_hash = 'f96f6fc8bcbbe523dc93339fdd130b3c'

client = TelegramClient('sticker_filter', api_id, api_hash)

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
                        print(f"Удалён стикер из приватного пака от @{target_username}")

client.start()
print("Скрипт запущен. Жду стикер от цели...")
client.run_until_disconnected()
