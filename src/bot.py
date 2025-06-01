import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import callback_navigation
from callback_navigation import router_navigation
from schedule_updater import lazy_process_students

logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
load_dotenv()
API_TOKEN = os.environ.get("BOT_TOKEN")  # Читаем токен из .env

bot = Bot(token=API_TOKEN)
callback_navigation.cl_bot = bot
dp = Dispatcher()


# Асинхронная задача, которая будет вызываться по таймеру
async def scheduler_task():
    """Периодически вызывает функцию расписания."""
    while True:
        # Вызываем логику обновления расписаний
        await lazy_process_students(bot)
        await asyncio.sleep(1800)

async def main():
    dp.include_router(router_navigation)
    callback_navigation.cl_bot = bot
    # Запускаем фоновую задачу
    asyncio.create_task(scheduler_task())

    # Запускаем "долгоживущий" процесс обработки апдейтов
    print("Bot")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
