from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]], resize_keyboard=True)

command_button = [
    [InlineKeyboardButton(text='Сделать рассылку', callback_data='send_malling')]
]
admin_commands = InlineKeyboardMarkup(inline_keyboard=command_button)


confirm_button = [
    [InlineKeyboardButton(text='Отправить', callback_data='send'),
     InlineKeyboardButton(text='Отмена', callback_data='dont_send')]
]
confirm_buttons = InlineKeyboardMarkup(inline_keyboard=confirm_button)
