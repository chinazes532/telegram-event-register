import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN

from handlers.user_message import router as user_router
from handlers.admin_message import router as admin_router

from database import create_db

async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
