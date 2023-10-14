import telebot
import cfg
import server_con
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import board_tree
import json
bot=telebot.TeleBot(token=cfg.TOKEN)
import personal_asks
from datetime import date
import text_editor



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


@bot.message_handler(commands=["start"])
def start_answer(message):
    bot.send_message(message.chat.id, "/Твой_Справочник\n/Хочу_в_Очередь_на_сдачу")

@bot.message_handler(commands=['Твой_Справочник'])
def book_answer(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for_newby_btn = InlineKeyboardButton(text="БСК", callback_data="bsk_0")
    studsovet_btn = InlineKeyboardButton(text="Студсовет", callback_data="studsovet")
    classrooms_btn = InlineKeyboardButton(text="Промежуточная аттестация", callback_data="session_0")
    hotels_btn =  InlineKeyboardButton(text="Общаги", callback_data="hotels")
    FAQ_btn =  InlineKeyboardButton(text="Частозадаваемые", callback_data="FAQ")
    personal_ask_btn = InlineKeyboardButton(text="Свой вопрос", callback_data="personal_ask")
    keyboard.add(for_newby_btn, studsovet_btn,classrooms_btn, hotels_btn, FAQ_btn, personal_ask_btn)
    bot.send_photo(message.chat.id, photo = open(f"logo.jpeg", "rb"), caption= "Привет, я могу помочь тебе разобраться с тем, как все у нас в вузе устроено\n", reply_markup=keyboard)


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



@bot.message_handler(commands=['Хочу_в_Очередь_на_сдачу'])
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


while 1:
    try:    
        bot.infinity_polling()
    except Exception:
        continue