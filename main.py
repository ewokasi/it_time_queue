#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import telebot
import cfg
import server_con
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle,InputTextMessageContent
import board_tree
import json
import forwarder
import booker
bot=telebot.TeleBot(token=cfg.TOKEN)



@bot.message_handler(commands=['start'])
def start_answer(message):
    btns = []

    btns.append([InlineKeyboardButton(text="Создать очередь для группы", callback_data="make_queue")])
    btns.append([InlineKeyboardButton(text="Создать очередь для 2-х групп", callback_data="make_double_queue")])
    btns.append([InlineKeyboardButton(text="Создать Группу", callback_data="create_group"),InlineKeyboardButton(text="Вступить в группу", callback_data="join_group")])
    keyboard = InlineKeyboardMarkup(btns, row_width=1)
    bot.send_message(chat_id=message.chat.id, text=f"{message.from_user.id} Привет, с моей помощью ты можешь организовать очередь на сдачу преподавателю\n\nВот ссылки на наши другие боты: //", reply_markup=keyboard)


@bot.inline_handler(lambda query: query.query == '#')
def query_text(inline_query):
    try:
        r = InlineQueryResultArticle('1', 'Костяков', InputTextMessageContent('hi'))
        r2 = InlineQueryResultArticle('2', 'DevSpot', InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['fw_settings'])
def settings_firewall(message):
     fw =[]
     fw.append([InlineKeyboardButton(text="Ваше Имя", callback_data="red_name")])
     fw.append([InlineKeyboardButton(text="Посмотреть все чаты", callback_data="all_chats")])
     fw.append([InlineKeyboardButton(text="Гайд", callback_data="fw_guide")])
     fw_kb = InlineKeyboardMarkup(fw, row_width=1)
     bot.send_message(message.chat.id, text = """Настойки файрволла. 
-Поменяйте Имя, которым будет подписано ваше сообщение
-Просмотр всех чатов, которым вы можете отправить сообщение
-Гайд по использованию файрволла для связи""", reply_markup=fw_kb)

@bot.message_handler(commands=['add_chat'])
def add_firewall(message):
    if message.text == "/add_chat":
        bot.send_message(message.chat.id,"Чтобы правильно добавить этот чат в сеть фаерволла, Укажите имя чата, оно должно быть уникальным и представляет вас как пользователя. \nПример: /add_chat Иванов Иван")
        return
    body = message.text.replace("/add_chat ", '', 1)
    if forwarder.add_chat(message.from_user.username, body, message.chat.id) == None:
        bot.send_message(message.chat.id, f"Чат с таким именем или ID уже существует. Попробуйте еще раз")
        return
    bot.send_message(message.chat.id, f"Добавлен новый чат. Его имя {body}. Если у вас несколько чатов, Другие пользователи будут обращаться к нему через {body}. Вы можете изменить это имя через /fw_settings")

@bot.callback_query_handler(func=lambda call: call.data.startswith('create_group'))
def start_answer(call):
    
    msg = bot.send_message(call.message.chat.id, "Введите номер вашей группы:")
    bot.register_next_step_handler(msg, server_con.create_group, call.from_user.id, call.from_user.username )



@bot.callback_query_handler(func=lambda call: call.data.startswith('join_group'))
def start_answer(call):
    
    msg = bot.send_message(call.message.chat.id, "Введите номер вашей группы:")
    bot.register_next_step_handler(msg, server_con.join_group, call.message.from_user.id, call.from_user.username )



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    board_tree.branch(call, bot)


@bot.message_handler(content_types=["text"])
def firewall_talk(message): 
    if message.text[0]!='@': return
    
    destination=message.text.split(sep=',')[0]
    mes = message.text.replace(destination, "", 1)
    mes=mes.replace(", ",'',1)
    text_to_talk = f"Вам сообщение от {forwarder.get_chat_name(message.chat.id)}: "+mes
    destination = destination.replace("@", '', 1)
    if forwarder.get_id(destination)==None: return
    id = forwarder.get_id(destination)
   
    bot.send_message(id, text_to_talk)
    bot.send_message(message.chat.id, "Сообщение отправлено")

while 1:
    try:    
        bot.infinity_polling()
    except Exception:
        continue