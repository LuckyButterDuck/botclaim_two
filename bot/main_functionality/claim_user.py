from aiogram import types
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot.database import add_user_from_malling
from bot.utils import bot

PHOTO_LINK = FSInputFile('media/photo_2023-12-10_20-27-04.jpg')


async def claim_user(chat_join: types.ChatJoinRequest):
    await chat_join.approve()
    try:
        await bot.send_photo(
            chat_join.from_user.id,
            photo=PHOTO_LINK,
            caption='<strong>👉НАБОР СОТРУДНИКОВ ПО ВСЕМУ СНГ\n\n💸ОПЛАТА ОТ <u>100 000</u> В НЕДЕЛЮ💸 '
                    '\n\n💎КУРЬЕР\n💎ВОДИТЕЛЬ\n💎СКЛАД\n\n❗️ВАЖНО</strong>\n<i>💵Есть реферальная программа приведи друга '
                    'и получи 2000 рублей сразу после устройства</i>\n\n\n🔮Чтобы узнать подробнее пишите:\n<a '
                    'href="https://telegra.ph/Rady-vas-privetstvovat-v-magazine-HOGWARTS-SHOP-12-04">HOGWARTS</a>'
        )
    except:
        pass


async def reg_user(message: types.Message, session_maker: sessionmaker):
    result = await add_user_from_malling(
        session_maker=session_maker,
        user_id=str(message.from_user.id),
        user_name=message.from_user.full_name
    )
    if result is not None:
        await message.answer(result)
