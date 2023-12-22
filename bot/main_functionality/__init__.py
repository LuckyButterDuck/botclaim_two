__all__ = ['register_user_handler']

import os
from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from .claim_user import claim_user, reg_user
from .admin_command import (
    login_admin,
    get_login,
    get_pass,
    start_constructe_malling,
    get_photo,
    get_text,
    send_or_no
)

from bot.structures import LoginAdminFSM, CreateMalling
from .antispam import ThrotlingMiddleware


def register_user_handler(router: Router):
    router.chat_join_request.register(claim_user, F.chat.id == int(os.getenv('CHANEL_ID')))
    router.message.register(reg_user, CommandStart())
    router.message.register(login_admin, Command('panel_admin'))
    router.message.register(get_login, LoginAdminFSM.get_login)
    router.message.register(get_pass, LoginAdminFSM.get_pass)
    router.callback_query.register(start_constructe_malling, F.data == 'send_malling')
    router.message.register(get_photo, CreateMalling.get_photo)
    router.message.register(get_text, CreateMalling.get_text)
    router.callback_query.register(send_or_no, CreateMalling.confirm_sending)
