import asyncio
from aiogram import Bot, Dispatcher, types
from config.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo_handler(message: types.Message):
    text = message.text
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())