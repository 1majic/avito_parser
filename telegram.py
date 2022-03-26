from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
# import timer
from aiogram.utils import executor

from m1 import main
from time import sleep
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_hi = KeyboardButton('Проверить наличие новых объявлений')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)

good_ids = ['']


bot = Bot(token='1931063261:AAFB6-d67vEQsef7_MvnW-e1wo8qS6o2YU0')
dp = Dispatcher(bot)


try:
    @dp.message_handler(commands=['start'])
    async def sendMessage(message: types.Message):
        while True:
            alls = main()
            for i in alls:
                await message.answer(f"{i.title}\n{i.price}{i.currency}\n{i.url}")
            sleep(200)
except:
    pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
