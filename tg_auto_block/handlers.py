from loguru import logger
from telethon import events, functions
from telethon.tl.types import InputPeerUser


@events.register(events.NewMessage)
@logger.catch
async def block_unknown_user(event):
    chat = await event.get_input_chat()
    if not isinstance(chat, InputPeerUser):
        return
    client = event.client
    sender_full = await client(functions.users.GetFullUserRequest(id=event.sender_id))
    sender = sender_full.user
    if sender.contact or sender.mutual_contact:
        return
    if not sender_full.common_chats_count:  # TODO
        client = event.client
        await client(functions.messages.DeleteHistoryRequest(event.chat_id, 0))
        await client(functions.contacts.BlockRequest(id=sender))
