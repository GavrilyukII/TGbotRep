import random
from random import randint
import model
from create_bot import bot
from aiogram import types
from aiogram.types import InputFile

async def start(message: types.Message):
    model.setCount(int(model.getUserCount()))
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} ✌!\nЭтот бот предназначен '
                                                 f'для игры в "КОНФЕТЫ🍭".\nВы с ботом по очереди берете конфеты со '
                                                 f'стола (всего 150).\nТот, кто взял последнюю конфету, выигрывает и '
                                                 f'получает замечательный приз.\nНо помни, за один ход можно взять '
                                                 f'не более 28 конфет⚠')
    model.setFirstTurn()
    first_turn = model.getFirstTurn()
    if first_turn:
        await playerTake(message)
    else:
        await enemyTurn(message)


async def playerTake(message: types.Message):
    await bot.send_message(message.from_user.id, f'{message.from_user.username}, возьмите конфеты, но не более 28')

async def playerTurn(message: types.Message):
    take = None
    if message.text.isdigit():
        if int(message.text) < 0 or int(message.text) > 28:
            await bot.send_message(message.from_user.id, 'Не стоит брать больше 28 конфет😈')
        else:
            take = int(message.text)
            model.setTake(int(message.text))
            model.setCount(model.getCount() - take)
            await bot.send_message(message.from_user.id, f'{message.from_user.username} взял {take} конфет, '
                                                         f'после чего на столе осталось {model.getCount()}')
            if model.checkWin():
                await bot.send_message(message.from_user.id, 'Коннер победил, Скайнет повержен!\nЕсли хотите сыграть '
                                                             'еще, введите команду /start\nА теперь твоя награда👇')
                path = InputFile('grud.jpg')
                await bot.send_photo(message.from_user.id, photo=path)
                return
            await enemyTurn(message)
    else:
        await bot.send_message(message.from_user.id, f"{message.from_user.username} введите количество конфет:")

async def enemyTurn(message: types.Message):
    count = model.getCount()
    take = count % 29 if count % 29 != 0 else random.randint(1, 28)
    model.setTake(take)
    model.setCount(count - take)
    await bot.send_message(message.from_user.id, f'Бот взял {model.getTake()}, на столе осталось '
                                                 f'{model.getCount()}')

    if model.checkWin():
        await bot.send_message(message.from_user.id, f'Скайнет ПОБЕДИЛ 🦴\nЕсли хотите сыграть еще, введите команду '
                                                     f'/start')
        pathend = InputFile('gachi.jpg')
        await bot.send_photo(message.from_user.id, photo=pathend)
        return
    await playerTake(message)
