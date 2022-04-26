from os import getenv
from pathlib import Path

import socks
from loguru import logger
from telethon import TelegramClient

from handlers import block_unknown_user

BASE_DIR = Path(__file__).parent
SESSION_DIR = BASE_DIR / 'session'
SESSION_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = getenv('APP_NAME', "TG_BOT")
PROXY_HOST = getenv('PROXY_HOST')
PROXY_PORT = int(getenv('PROXY_PORT', 8087))

api_id = int(getenv('api_id'))
api_hash = getenv('api_hash')
bot_token = getenv('bot_token')
phone = getenv('phone')
bot_owner = getenv('bot_owner')

proxy = None
if PROXY_HOST:
    proxy = (socks.SOCKS5, PROXY_HOST, PROXY_PORT)

client = TelegramClient(str(SESSION_DIR / APP_NAME),
                        api_id=api_id,
                        api_hash=api_hash,
                        proxy=proxy,
                        flood_sleep_threshold=20) \
    .start(phone=lambda: phone)

if __name__ == '__main__':
    logger.info("Starting Connection")
    with client:
        logger.info("Connection Established")

        # docker plugin
        client.add_event_handler(block_unknown_user)

        # client.loop.run_until_complete(start_up_msg(client))
        client.run_until_disconnected()
