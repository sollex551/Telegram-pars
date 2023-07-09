import os
import sqlite3
from aiogram.types import Document, ContentTypes
from aiogram.dispatcher.filters import ContentTypeFilter

from aiogram import Bot, types
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeFilename


async def parse_messages(api_id, api_hash, channel_username):
    async with TelegramClient('session_name', api_id, api_hash) as client:
        entity = await client.get_entity(channel_username)
        messages = await client.get_messages(entity, limit=100)

        conn = sqlite3.connect('message.db', isolation_level=None)
        cursor = conn.cursor()

        for message in messages:
            cursor.execute('''
                REPLACE INTO messages(message_id, message_text) VALUES(?, ?)
                ''', (message.id, message.text))

            if message.photo:
                photo = message.photo
                # Сохранение фото в папку "media"
                file_path = os.path.join('media', f'photo_{photo.id}.jpg')
                await client.download_media(photo, file_path)

                cursor.execute('''
                               REPLACE INTO messages(message_id, message_text, photo_file_path) 
                               VALUES(?, ?, ?)
                               ''', (message.id, message.text, file_path))

            if message.video:
                # Сохранение видео в папку "media"
                file_path = os.path.join('media', f'video_{message.video.id}.mp4')
                await client.download_media(message.video, file_path)

                cursor.execute('''
                                   REPLACE INTO messages(message_id, message_text, video_file_path) 
                                   VALUES(?, ?, ?)
                                   ''', (message.id, message.text, file_path))

            if message.document:
                file_name = None
                for attribute in message.document.attributes:
                    if isinstance(attribute, DocumentAttributeFilename):
                        file_name = attribute.file_name
                        break

                if file_name is not None:
                    file_path = os.path.join('media', file_name)
                    await client.download_media(message.document, file_path)

                    cursor.execute('''
                        REPLACE INTO messages(message_id, message_text, file_file_path) 
                        VALUES(?, ?, ?)
                        ''', (message.id, message.text, file_path))



                    # Добавьте обработку других типов медиа, если необходимо

        conn.commit()
        cursor.close()
        conn.close()


async def main(user_name):
    # Ваши данные API
    api_id = 'YOUR_API_ID'
    api_hash = 'YOUR_API_HASH'
    channel_username = user_name

    # Имя канала для парсинга сообщений

    await parse_messages(api_id, api_hash, channel_username)

# Здесь должен быть код, который вызывает функцию main()
