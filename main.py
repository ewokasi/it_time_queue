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
import personal_asks
import text_editor

bot=telebot.TeleBot(token=cfg.TOKEN)

@bot.callback_query_handler(func=lambda call: call.data.startswith('booker'))
def booker_start(call):
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    for_newby_btn = InlineKeyboardButton(text="БСК", callback_data="Bbsk_0")
    studsovet_btn = InlineKeyboardButton(text="Студсовет", callback_data="Bstudsovet")
    classrooms_btn = InlineKeyboardButton(text="Промежуточная аттестация", callback_data="Bsession_0")
    hotels_btn =  InlineKeyboardButton(text="Общаги", callback_data="Bhotels")
    FAQ_btn =  InlineKeyboardButton(text="Частозадаваемые", callback_data="BFAQ")
    personal_ask_btn = InlineKeyboardButton(text="Свой вопрос", callback_data="Bpersonal_ask")
    keyboard.add(for_newby_btn, studsovet_btn,classrooms_btn, hotels_btn, FAQ_btn, personal_ask_btn)
    bot.send_photo(call.message.chat.id, photo = open(f"logo.jpeg", "rb"), caption= "Привет, я могу помочь тебе разобраться с тем, как все у нас в вузе устроено\n", reply_markup=keyboard)
    


def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

def read_dict(name):
    with open(str(name) + '.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data

@bot.message_handler(commands=['ask'])
def send_welcome(message):
    msg = bot.reply_to(message, "Вы можете отправить вопрос в этот чат, после чего вам ответит оператор")
    bot.register_next_step_handler(msg, personal_asks.get_question, bot)

@bot.message_handler(commands=['joinCrew'])
def add_to_FAQCrew(message):
    personal_asks.add_operator(message, bot)

@bot.message_handler(commands=['exitCrew'])
def exit_FAQCrew(message):
    personal_asks.remove_operator(message, bot)


@bot.message_handler(commands=["addAdmin"])
def add_admin(message):
    file = open(r"admins.txt")
    admins = file.read().splitlines()
    file.close()
    if message.chat.username in admins:
        file = open(r"admins.txt", "a")
        file.write("\n"+message.text.replace("/addAdmin ", "", 1))
        file.close()
    bot.send_message(message.chat.id,  "Добавлен новый админ "+ message.text.replace("/addAdmin ", "", 1))

@bot.callback_query_handler(func=lambda call: call.data.startswith('fw'))
def start_answer(call):
     fw =[]
     fw.append([InlineKeyboardButton(text="Ваше Имя", callback_data="red_name")])
     fw.append([InlineKeyboardButton(text="Посмотреть все чаты", callback_data="all_chats")])
     fw.append([InlineKeyboardButton(text="Гайд", callback_data="fw_guide")])
     fw_kb = InlineKeyboardMarkup(fw, row_width=1)
     bot.send_message(call.message.chat.id, text = """Настойки файрволла. 
-Поменяйте Имя, которым будет подписано ваше сообщение
-Просмотр всех чатов, которым вы можете отправить сообщение
-Гайд по использованию файрволла для связи""", reply_markup=fw_kb)


@bot.callback_query_handler(func=lambda call: call.data.startswith('queue'))
def start_answer(call):
    btns = []

    btns.append([InlineKeyboardButton(text="Создать очередь для группы", callback_data="make_queue")])
    btns.append([InlineKeyboardButton(text="Создать очередь для 2-х групп", callback_data="make_double_queue")])
    btns.append([InlineKeyboardButton(text="Создать Группу", callback_data="create_group"),InlineKeyboardButton(text="Вступить в группу", callback_data="join_group")])
    keyboard = InlineKeyboardMarkup(btns, row_width=1)
    bot.send_message(chat_id=call.message.chat.id, text=f"{call.message.from_user.id} Привет, с моей помощью ты можешь организовать очередь на сдачу преподавателю\n\nВот ссылки на наши другие боты: //", reply_markup=keyboard)



@bot.message_handler(commands=["help"])
def help_answer(message):
    file = open(r"admins.txt")
    admins = file.read().splitlines()
    file.close()
    if message.chat.username in admins:
    
        bot.send_message(message.chat.id, text = """В боте есть две роли: Админы и операторы. Админы могут редактировать содержимое справочника и добавлять других админов, а операторы могут отвечать на вопросы пользователей.\nЧтобы добавить Админа укажите его юзернейм без @ - "/addAdmin Anton"\n Чтобы стать/перестать быть оператором - "/joinCrew" / "/exitCrew"\nчтобы обновить информацию в боте отправьте в чат docx документ (очистив всё форматирование) с определенным названием:\n
Для бск - "БСК.docx"\n
Для Промежуточной аттестации - "Промежуточная аттестация.docx"\n
Для Перевода на другой факультет -"Перевод на другой факультет.docx\"
Для матпомощи - "Матпомощь.docx\"\n
Для стипендии - "Стипендия.docx\"\n
Для промежуточной аттестации - "Промежуточная аттестация.docx"\n
Для ВУЦ - "ВУЦ.docx"\n
Для перевода на бюджет = "Перевод на бюджет.docx"\n
Для истории ГУАП - "История ГУАП"\n
Для Обновления инфы о деканатах - "Деканат 1.docx" или "Деканат 2.docx","Деканат ФПТИ.docx","Деканат ВУЦ.docx"\n""")
    else:
         bot.send_message(message.chat.id, text = 'Чтобы начать работу бота - пиши "/start"\nЧтобы задать вопрос оператору - "/ask"')

#######################


@bot.message_handler(commands=["start"])
def starter(message):
    btns = []
    btns.append( [InlineKeyboardButton(text="Очереди", callback_data="queue"), InlineKeyboardButton(text="Справочник", callback_data="booker")]) 
    btns.append( [InlineKeyboardButton(text="Фаерволл", callback_data="fw")])
    kb = InlineKeyboardMarkup(btns)
    bot.send_message(message.chat.id, "Выберите бота для работы", reply_markup=kb)

@bot.message_handler(content_types=['document', 'file']) # list relevant content types
def edit_info(message):
    file = open(r"admins.txt")
    admins = file.read().splitlines()
    file.close()
    if message.chat.username not in admins: return
    file_name = message.document.file_name
    if file_name.split(sep = ".")[1]!="docx":
        print("denied")
        return 1
    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    multistring= text_editor.getText(file_name)
    print("------------------multistring-------------",multistring)
    text_editor.update_text(file_name.split(sep = ".")[0], multistring)
    

    
    bot.send_message(message.chat.id, text=file_name + ": сохранена информация")




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
    if call.data[0]!="B":
     board_tree.branch(call, bot)
    else:
        booker.branch(call , bot)

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
            bot.polling()
        except Exception:
            continue