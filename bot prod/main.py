import config
from aiogram import Bot,Dispatcher,types, executor
from aiogram.dispatcher.filters import Text
from db import Database
from datetime import datetime
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
import keyboard


user_data = {}
bot = Bot(token=config.TOKEN)
kd = Dispatcher(bot)
db = Database('shop.db')

    
async def update_num_text(message: types.Message, new_value: int):
    with suppress(MessageNotModified):
        await message.edit_text(f"Укажите число: {new_value}", reply_markup=keyboard.get_keyboard())

@kd.message_handler(commands="menu")
async def cmd_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Мой баланс", callback_data="balance_value"))
    keyboard.add(types.InlineKeyboardButton(text="Пополнить баланс", callback_data="balance_add"))
    keyboard.add(types.InlineKeyboardButton(text="Список товаров", callback_data="towars"))
    keyboard.add(types.InlineKeyboardButton(text="История покупок", callback_data="historybuy"))
    await message.answer("Привет!\nВыберите кнопку под сообщением чтобы продолжить.", reply_markup=keyboard)
    
    
@kd.callback_query_handler(text="historybuy")
async def balance(call: types.CallbackQuery):
    historybuy = db.my_history(call.from_user.id)
    await call.message.answer(historybuy)

        
@kd.callback_query_handler(text="balance_value")
async def balance(call: types.CallbackQuery):
    balances = db.get_balance(call.from_user.id)
    await call.message.answer(f"Ваш баланс: {balances} $ ")
    await call.answer(text=(f"Ваш баланс: {balances} $ "), show_alert=True)
    
@kd.callback_query_handler(text="balance_add")
async def balance_add(call: types.CallbackQuery):
    await call.message.answer("Для пополнения баланса отправь мне /addbalance")
    
@kd.message_handler(commands="addbalance")
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите насколько хотите пополнить баланс: 0", reply_markup=keyboard.get_keyboard())

@kd.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "incr":
        user_data[call.from_user.id] = user_value+100
        await update_num_text(call.message, user_value+100)
    elif action == "decr":
        user_data[call.from_user.id] = user_value-100
        await update_num_text(call.message, user_value-100)
    elif action == "finish":
        await call.message.edit_text(f"Вы успешно пополнили баланс на: {user_value}")
        db.add_balance(call.from_user.id, user_value)
    await call.answer()
    
@kd.callback_query_handler(text="towars")
async def balance_add(call: types.CallbackQuery):
    towars_name = db.tow_name()
    towars_desc = db.tow_desc()
    towars_price = db.tow_price()
    tow_name = []
    tow_desc = []
    tow_price = []
    
    for string in towars_name:
        string = str(string)
        cleaned_string = string.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()
        tow_name.append(cleaned_string)
    for string in towars_desc:
        string = str(string)
        cleaned_string = string.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()
        tow_desc.append(cleaned_string)
    for string in towars_price:
        string = str(string)
        cleaned_string = string.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()
        tow_price.append(cleaned_string)
    
    await call.message.answer(f"Товары:\n1) {tow_name[0]}, {tow_desc[0]}, цена:{tow_price[0]} $\n2) {tow_name[1]}, {tow_desc[1]}, цена:{tow_price[1]} $\n3) {tow_name[2]}, {tow_desc[2]}, цена:{tow_price[2]} $ ")
    await call.message.answer(text= 'Выбери действие.',
                        reply_markup = keyboard.main_kb)

@kd.message_handler(text = "Купить 1 товар")
async def tow1(message: types.Message):
    balances = db.get_balance(message.from_user.id)
    towars_price = db.tow_price()
    tow_price = []
    date = datetime.now()
    item_id = 1
    
    for string in towars_price:
        string = str(string)
        cleaned_string = string.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()
        tow_price.append(cleaned_string)
    
    if int(balances) < int(tow_price[0]):
        await message.reply("У вас не хватает средств!")
    elif int(balances) > int(tow_price[0]):
        db.history_add(message.from_user.id, item_id, date)
        db.remove_balance(message.from_user.id,tow_price[0])
        await message.reply("Вы успешно купили товар под номером 1!")
        await message.delete_reply_markup()
    
@kd.message_handler(text = "Купить 2 товар")
async def tow1(message: types.Message):
    balances = db.get_balance(message.from_user.id)
    towars_price = db.tow_price()
    tow_price = []
    date = datetime.now()
    item_id = 2
    
    for string in towars_price:
        string = str(string)
        cleaned_string = string.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()
        tow_price.append(cleaned_string)
    
    if int(balances) < int(tow_price[1]):
        await message.reply("У вас не хватает средств!")
    elif int(balances) > int(tow_price[1]):
        db.history_add(message.from_user.id, item_id, date)
        db.remove_balance(message.from_user.id,tow_price[1])
        await message.reply("Вы успешно купили товар под номером 2!")
        await message.delete_reply_markup()
        
@kd.message_handler(text = "Купить 3 товар")
async def tow1(message: types.Message):
    balances = db.get_balance(message.from_user.id)
    towars_price = db.tow_price()
    tow_price = []
    date = datetime.now()
    item_id = 3
    
    for string in towars_price:
        string = str(string)
        cleaned_string = string.replace("(", "").replace(")", "").replace(",", "").replace("'", "").strip()
        tow_price.append(cleaned_string)
    
    if int(balances) < int(tow_price[2]):
        await message.reply("У вас не хватает средств!")
    elif int(balances) > int(tow_price[2]):
        db.history_add(message.from_user.id, item_id, date)
        db.remove_balance(message.from_user.id,tow_price[2])
        await message.reply("Вы успешно купили товар под номером 3!")
        await message.delete_reply_markup()



@kd.message_handler()
async def process_message(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)


if __name__ == "__main__":
    print("Starting...", end='')
    executor.start_polling(kd, skip_updates=True)
    