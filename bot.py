import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import datetime

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = '7713559661:AAH3YmDRWoWJUh8wHyQO99_Hx5Eav-h_qzs'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def show_price(message: types.Message, price):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Посмотреть цену"))
    # builder.add(types.KeyboardButton(text="Остановить"))
    await message.answer(f'Начальная цена: {price}', reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text == "Посмотреть цену")
async def get_price(message: types.Message):
    url = 'https://steamcommunity.com/market/priceoverview/?appid=730&currency=5&market_hash_name=Shanghai%202024%20Viewer%20Pass'

    resp = requests.get(url)
    price = resp.text.split('"')[5]

    await show_price(message, price)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await get_price(message)

    while True:
        if datetime.datetime.now().hour in [6, 10, 14, 18, 20]:
            await get_price(message)
            await asyncio.sleep(7079)
        await asyncio.sleep(120)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
