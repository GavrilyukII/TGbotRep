from aiogram.dispatcher import Dispatcher
import commands

def registred_handlers (dp: Dispatcher):
    dp.register_message_handler(commands.start, commands=['start'])
    # dp.register_message_handler(commands., commands=['help'])
    dp.register_message_handler(commands.playerTurn)
