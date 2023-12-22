import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.database import get_users
from bot.keyboards import admin_commands, cancel, confirm_buttons
from bot.structures import LoginAdminFSM, CreateMalling
from bot.utils import bot


async def login_admin(message: types.Message, state: FSMContext):
    await message.answer('Введите логин:', reply_markup=cancel)
    await state.set_state(LoginAdminFSM.get_login)


async def get_login(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        return
    if message.text == os.getenv('ADMIN_LOGIN'):
        await message.answer('Введите пароль:', reply_markup=cancel)
        await state.set_state(LoginAdminFSM.get_pass)
    else:
        await message.answer('Логин не верный. Попробуйте ещё раз')


async def get_pass(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        return
    if message.text == os.getenv('ADMIN_PASS'):
        await state.clear()
        return await admin_command(message)
    else:
        await message.answer('Логин не верный. Попробуйте ещё раз')


async def admin_command(message: types.Message):
    await message.answer('Вход выполнен! Команды:', reply_markup=admin_commands)


async def start_constructe_malling(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Пришлите фотографию к посту', reply_markup=cancel)
    await state.set_state(CreateMalling.get_photo)


async def get_photo(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[0].file_id
    except:
        photo = None

    if message.text == 'Отмена':
        await state.clear()
        return await admin_command(message)
    if photo is None:
        await message.answer('Рассылка будет без фото. Пришлите текст рассылки', reply_markup=cancel)
        await state.set_state(CreateMalling.get_text)
        await state.update_data(photo=photo)
    else:
        await state.update_data(photo=photo)
        await message.answer('Фото добавлено. Пришлите текст рассылки', reply_markup=cancel)
        await state.set_state(CreateMalling.get_text)


async def get_text(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        return await admin_command(message)
    await message.answer('Текст получен')
    data = await state.get_data()
    photo = data['photo']
    text = message.text
    await state.update_data(text=text)
    if photo is None:
        await message.answer(text, reply_markup=confirm_buttons)
    else:
        await message.answer_photo(photo, caption=text, reply_markup=confirm_buttons)
    await state.set_state(CreateMalling.confirm_sending)


async def send_or_no(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    if str(call.data) == 'not_send':
        await call.answer('Отменено')
        await state.clear()
        return await admin_command(call.message)
    await call.answer('Отправка...')
    data = await state.get_data()
    photo = data['photo']
    text = data['text']
    users = await get_users(session_maker)
    if photo is not None:
        for user in users:
            try:
                _text = text.replace('username', user[1])
                user_id = int(user[0])
                await bot.send_photo(user_id, photo=photo, caption=_text)
            except:
                continue
    else:
        for user in users:
            try:
                _text = text.replace('username', user[1])
                user_id = int(user[0])
                await bot.send_message(user_id, _text)
            except:
                continue
    await state.clear()
    await call.message.answer('Рассылка сделана')
    return await admin_command(call.message)
