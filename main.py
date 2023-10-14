import telebot
import cfg
import server_con
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import board_tree
import json
bot=telebot.TeleBot(token=cfg.TOKEN)



@bot.message_handler(commands=['start'])
def start_answer(message):
    btns = []

    btns.append([InlineKeyboardButton(text="Создать очередь для группы", callback_data="make_queue")])
    btns.append([InlineKeyboardButton(text="Создать очередь для 2-х групп", callback_data="make_double_queue")])
    btns.append([InlineKeyboardButton(text="Создать Группу", callback_data="create_group"),InlineKeyboardButton(text="Вступить в группу", callback_data="join_group")])
    keyboard = InlineKeyboardMarkup(btns, row_width=1)
    bot.send_message(chat_id=message.chat.id, text=f"{message.from_user.id} Привет, с моей помощью ты можешь организовать очередь на сдачу преподавателю\n\nВот ссылки на наши другие боты: //", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('create_group'))
def start_answer(call):
    
    msg = bot.send_message(call.message.chat.id, "Введите номер вашей группы:")
    bot.register_next_step_handler(msg, server_con.create_group, call.message.from_user.id, call.from_user.username )


@bot.callback_query_handler(func=lambda call: call.data.startswith('join_group'))
def start_answer(call):
    
    msg = bot.send_message(call.message.chat.id, "Введите номер вашей группы:")
    bot.register_next_step_handler(msg, server_con.join_group, call.message.from_user.id, call.from_user.username )



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    board_tree.branch(call, bot)



while 1:
    try:    
        bot.infinity_polling()
    except Exception:
        continue