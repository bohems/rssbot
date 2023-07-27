import datetime
import json
import logging

from telethon import TelegramClient, events
from datetime import datetime

logging.basicConfig(filename='exceptions.log', level=logging.ERROR)

with open('config.json') as c:
    config = json.load(c)

api_id = config["telegram_access_keys"]["api_id"]
api_hash = config["telegram_access_keys"]["api_hash"]
bot_token = config["telegram_access_keys"]["bot_token"]

tracked_communities = config["members"]["tracked_communities"]
middle_receiver = config["members"]["middle_receiver"]
final_receiver = config["members"]["final_receiver"]

client = TelegramClient('client', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage(chats=tuple(tracked_communities)))
async def handler(event):
    try:
        await client.forward_messages(middle_receiver, event.message)
    except Exception as e:
        logging.error(f"[{datetime.now().strftime('%H:%M:%S')}] Ошибка при пересылке сообщения: {e}")


@bot.on(events.NewMessage(chats=middle_receiver))
async def bot_handler(event):
    try:
        await bot.forward_messages(final_receiver, event.message)
    except Exception as e:
        logging.error(f"[{datetime.now().strftime('%H:%M:%S')}] Ошибка при пересылке сообщения: {e}")

def main():
    with client:
        client.run_until_disconnected()


if __name__ == '__main__':
    main()
