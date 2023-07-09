from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from get_id import *
from pars import *

try:
    # Создание экземпляров бота и диспетчера
    bot = Bot(token='your_bot_token')
    dp = Dispatcher(bot)

    # Создание подключения к базе данных
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()


    async def send_messages_to_channel(channel_id):
        # Получаем все сообщения из базы данных
        cursor.execute(
            "SELECT message_id, message_text, photo_file_path, video_file_path, file_file_path FROM messages")
        messages = cursor.fetchall()

        # Отправка сообщений в указанный канал
        for message_data in messages:
            try:
                message_id, message_text, photo_file_path, video_file_path, file_file_path = message_data

                # Отправка медиафайлов (если есть) вместе с текстом сообщения
                if photo_file_path:
                    photo = types.InputFile(photo_file_path)
                    await asyncio.sleep(3)
                    await bot.send_photo(channel_id, photo, caption=message_text, parse_mode='Markdown')
                if video_file_path:
                    video = types.InputFile(video_file_path)
                    await asyncio.sleep(3)
                    await bot.send_video(channel_id, video, caption=message_text, parse_mode='Markdown')
                if file_file_path:
                    file = types.InputFile(file_file_path)
                    await asyncio.sleep(3)
                    await bot.send_document(channel_id, file, caption=message_text, parse_mode='Markdown')
                if not any([photo_file_path, video_file_path, file_file_path]):
                    await asyncio.sleep(3)
                    await bot.send_message(channel_id, message_text, parse_mode='Markdown')

                if photo_file_path:
                    os.remove(photo_file_path)
                if video_file_path:
                    os.remove(video_file_path)
                if file_file_path:
                    os.remove(file_file_path)

            except Exception as e:
                print(f'Ошибка при отправке сообщения: {str(e)}')

        conn.commit()
        conn.close()


    # Обработчик команды /start
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await message.reply("Привет! Пожалуйста, отправь ссылку на канал, с которого хочешь парсить сообщения ")


    # Обработчик текстового сообщения с ссылкой на канал
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def process_channel_link(message: types.Message):
        if message.text.startswith('https://t.me/'):
            # Получаем ссылку на канал
            parts = message.text.split()
            if len(parts) == 2:
                channel_link, target_channel_id = parts

                await main(channel_link)

                await message.reply("Парсинг сообщений и добавление в базу данных завершено.")
                id = gi(channel_link)
                await send_messages_to_channel(id)

                await message.reply("Все сообщения были отправлены в целевой канал и база данных очищена.")
            else:
                await message.reply(
                    "Пожалуйста, отправь ссылку на канал в правильном формате и укажи идентификатор целевого канала через пробел.")

        # Запуск бота


    if __name__ == '__main__':
        executor.start_polling(dp)

except Exception as e:
    print('Ошибка')
