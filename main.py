from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import asyncio, aioschedule, sqlite3
from datetime import datetime, timedelta

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
#список пользователей, заменить на БД
users = []
with open('users.txt') as file:
    users = list(map(int, file.readlines()))

async def mess():
    conn = sqlite3.connect('FACES.db')
    cur = conn.cursor()
    # за какое время нужен отчет о пришедших
    DELTA_TIME = 2
    # определяем разницу во времени с текущего времени
    delta = datetime.now() - timedelta(hours=DELTA_TIME)
    # делаем выборку
    cur.execute('''SELECT name, date FROM faces
                    JOIN attend3 
                    WHERE faces.userid = attend3.userid AND
                     date>? AND date <?;''', (delta, datetime.now()))
    m = list(map(lambda x: x[0] + ': ' + datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f').strftime("%d.%m.%Y, %H:%M:%S"), cur.fetchall()))
    #m = cur.fetchall()
    #print(m)
    #TODO Добавить отправку отсутствующих
    cur.execute('''SELECT name FROM faces 
                    WHERE NOT EXISTS 
                    SELECT userid FROM attend3
                    WHERE date>? AND date <?
                    ;''', (delta, datetime.now()))
    #Сделать для нескольких пользователей - получателей
    for user in users:
        message = '\n'.join(m)
        await bot.send_message(user, message)

async def scheduler():
    #aioschedule.every().day.at("10:00").do(mess)
    aioschedule.every(1).minutes.do(mess)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


#Обработка старта
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global users

    if message.chat.id not in users:
        #сохранение пользователя
        print((message.chat.id))
        users += [message.chat.id]
        with open('users.txt', 'a') as file:
            file.write(str(message.chat.id) + '\n')

    await message.reply("Привет!")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
