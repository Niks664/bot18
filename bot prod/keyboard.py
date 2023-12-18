from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

main_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
button_1 = KeyboardButton(text='Купить 1 товар')
button_2 = KeyboardButton(text ="Купить 2 товар")
button_3 = KeyboardButton(text ="Купить 3 товар")
button_4 = KeyboardButton(text ="/menu")


main_kb.add(button_1).add(button_2).add(button_3).add(button_4)

def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="-100", callback_data="num_decr"),
        types.InlineKeyboardButton(text="+100", callback_data="num_incr"),
        types.InlineKeyboardButton(text="Пополнить", callback_data="num_finish")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
