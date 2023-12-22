from aiogram.fsm.state import StatesGroup, State


class LoginAdminFSM(StatesGroup):
    get_login = State()
    get_pass = State()


class CreateMalling(StatesGroup):
    get_photo = State()
    get_text = State()
    confirm_sending = State()
