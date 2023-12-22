import os
from aiogram import Bot

bot = Bot(token=os.getenv('token'), parse_mode='HTML')
