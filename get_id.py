import asyncio

from telethon.sync import TelegramClient


async def get_channel_id(api_id, api_hash, channel_username):
    async with TelegramClient('session_name', api_id, api_hash) as client:
        entity = await client.get_entity(channel_username)
        channel_id = entity.id
        return channel_id


async def gi(link):
    api_id = 'YOUR_ID'
    api_hash = 'YOUR_HASH'
    channel_username = link

    channel_id = await get_channel_id(api_id, api_hash, channel_username)
    return -100+channel_id


