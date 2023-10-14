from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import telebot
import server_con
import json
import text_editor
import texts
import personal_asks

def push_to_users(msg ,id, call,bot):
    data = server_con.get_users_groups(id, call.from_user.username)
    btns= []
    btns.append([InlineKeyboardButton(text="Встать", callback_data=f"join_{call.data.split(sep='_')[1]}")])
    keyboard = InlineKeyboardMarkup(btns, row_width=1)
    for u in data[0]['users']:   
       mess= bot.send_message(chat_id=u['telegramId'], text = msg, reply_markup=keyboard)
      
       server_con.add_message(call.data.split(sep='_')[1], str(mess.id))
      
def get_user_groups(group):
    return

def branch(call, bot):
    text = "Попробуй еще раз, что-то пошло не так (\n"
    content = text_editor.read_dict('texts')
    btns = []
    group = server_con.get_users_groups(user_id=call.from_user.id, username = call.from_user.username)
    print(group)
    if "make_queue" in call.data:
        text="Выберите группу для которой организуется сдача"
        for g in group:
            btns.append([InlineKeyboardButton(text=g['uniqId'], callback_data=f"group_{g['uniqId']}")])

    if "group_" in call.data:
        gr = call.data.split(sep='_')[1]
        server_con.create_queue(call.from_user.id, gr, call.from_user.username)
        push_to_users("Пора вставать в очередь", call.from_user.id, call,bot)
        text = "Когда будете готовы, сдавайте работу."

       
        # btns.append([InlineKeyboardButton(text="Сдал", callback_data=f"done_{call.data.split(sep='_')[1]}")])
        # btns.append([InlineKeyboardButton(text="На новый круг", callback_data=f"ring_{call.data.split(sep='_')[1]}")])
    if "join" in call.data:
        gr = call.data.split(sep='_')[1]
       
        server_con.add_user_to_queue(gr, call.from_user.id, call.from_user.username)
        btns = []
        btns.append([InlineKeyboardButton(text="Сдал", callback_data=f"done_{call.data.split(sep='_')[1]}")])
        btns.append([InlineKeyboardButton(text="На новый круг", callback_data=f"ring_{call.data.split(sep='_')[1]}")])
        btns.append([InlineKeyboardButton(text="Просмотр Очереди", callback_data=f"refresh_{call.data.split(sep='_')[1]}")])
        kd = InlineKeyboardMarkup(btns, row_width=2)
        messages=server_con.get_messages_id(gr, call.message.from_user.id, call.message.from_user.username)
        text = server_con.get_queue(call.message.from_user.id, gr, call.message.from_user.username)
        text = json.loads(text)
        outp="Чтобы покинуть очередь - Сдал\nЕсли препод отправил исправлять - Новый круг."
       
        # user_id= server_con.get_all_users_in_group(call.message.from_user.id ,gr)
        # for user in user_id:
        bot.send_message(chat_id=call.message.chat.id, text = outp, reply_markup=kd)
            
            
        bot.answer_callback_query( call.id, "Вы добавлены в конец очереди", show_alert= True)
       
        return
        
    
    #начало ветвлений
    if "menu" == call.data:
        btns.append( [InlineKeyboardButton(text="БСК", callback_data="bsk_0"), InlineKeyboardButton(text="Студсоветы", callback_data="studsovet")]) 
        btns.append( [ InlineKeyboardButton(text="Промежуточная аттестация", callback_data="session_0") , InlineKeyboardButton(text="Общаги", callback_data="hotels")])
        btns.append( [InlineKeyboardButton(text="Частозадаваемые", callback_data="FAQ")])
        btns.append([InlineKeyboardButton(text="Свой вопрос", callback_data="personal_ask")])
        text = "Привет, я могу помочь тебе разобраться с тем, как все у нас в вузе устроено\n"
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(f"logo.jpeg", "rb")))

    if "bsk" in call.data:
        btns, text= text_editor.gen_form(content["БСК"], "bsk", call)
        btns.append([InlineKeyboardButton(text="Назад", callback_data="menu")]) 
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(f"card.jpg", "rb")))
    if "personal_ask" in call.data:
            text = "Отправьте боту в чат команду /ask. Бот предложит вам задать ваш вопрос и передаст оператору. Ответ вы получите в этот чат."
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="menu")])   

    elif "studsovet" in call.data:
        text = "У каждого факультета в нашем вузе есть свой студсовет. Присоединяйся, ведь учиться вместе интересней. Ссылки на ВК ты можешь получить по кнопкам:"
        btns.append([InlineKeyboardButton("Общий студсовет ГУАП", url='https://vk.com/studsovguap')])
        btns.append([InlineKeyboardButton("Студсовет 1 Института", url='https://vk.com/guap_ssi_1'), InlineKeyboardButton("Студсовет 2 Института", url='https://vk.com/guap.ssi2')])
        btns.append([InlineKeyboardButton("Студсовет 3 Института", url='https://vk.com/studsovet_uyutno_3'), InlineKeyboardButton("Студсовет 4 Института", url='https://vk.com/guap_ss4')])
        btns.append([InlineKeyboardButton("Студсовет 6 Института", url='https://vk.com/shesterka_suai'), InlineKeyboardButton("Студсовет 8 Института", url="https://vk.com/guapstudsovet8")])
        btns.append([InlineKeyboardButton("Студсовет ФПТИ", url='https://vk.com/ssi_fpti'), InlineKeyboardButton("Студсовет 12 Института", url='https://vk.com/12fak')])
        btns.append([InlineKeyboardButton(text="Назад", callback_data="menu")]) 
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(f"studsovet.jpeg", "rb")))
    elif "session" in call.data:
        btns, text = text_editor.gen_form(content["Промежуточная аттестация"],"session", call)
        btns.append( [InlineKeyboardButton(text="Назад", callback_data="menu")]) 
    

    
    elif "hotels" in call.data:
        btns.append( [InlineKeyboardButton(text="№1, пр. Маршала Жукова, д. 24", callback_data="hotels_№1")]) 
        btns.append( [InlineKeyboardButton(text="№2, ул. Передовиков, д. 13", callback_data="hotels_№2")]) 
        btns.append( [InlineKeyboardButton(text="№3, ул. Варшавская, д. 8", callback_data="hotels_№3")]) 
        btns.append( [InlineKeyboardButton(text="Вопросы", callback_data="hotels_faq")]) 
        btns.append( [InlineKeyboardButton(text="Назад", callback_data="menu")]) 
        text = "Всего у ГУАПа 3 общежития:"

        if "hotels_№"  in call.data:
            btns.clear()
            i = int(call.data[-1])
            text = texts.hotels[f"{i}"][0]
            btns.append( [InlineKeyboardButton(text="Группа в вк", url=texts.hotels[f"{i}"][1])]) 
            btns.append( [InlineKeyboardButton(text="Больше фоток", url=texts.hotels[f"{i}"][2])]) 
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="hotels")]) 
            bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(texts.hotels[f"{i}"][3], "rb")))

        if "hotels_faq" == call.data:
            btns.clear()
            text = texts.hotels["faq"][0]
            btns.append( [InlineKeyboardButton(text="1/2 >>", callback_data="hotels_faq_1")]) 
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="hotels")]) 
        if "hotels_faq_1" == call.data:
            btns.clear()
            text = texts.hotels["faq"][1]
            btns.append( [InlineKeyboardButton(text="2/2 <<", callback_data="hotels_faq")]) 
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="hotels")]) 
    
    elif "FAQ" in call.data:
        btns.append( [InlineKeyboardButton(text="Контакты деканатов", callback_data="FAQ_dec") ,InlineKeyboardButton(text="Военная кафедра", callback_data="FAQ_voenka_0")]) 
        btns.append( [InlineKeyboardButton(text="Про стипендию", callback_data="FAQ_stipendiya_0"), InlineKeyboardButton(text="История ГУАП", callback_data="FAQ_history_0")])
        btns.append( [InlineKeyboardButton(text="Перевод на бюджет", callback_data="FAQ_перевод_на_бюджет_0")])  
        btns.append( [InlineKeyboardButton(text="Назад", callback_data="menu")]) 
    
        text = "Раздел FAQ"

        if "stipendiya" in call.data:
            btns, text = text_editor.gen_form(content["Стипендия"], "FAQ_stipendiya", call)
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="FAQ")])
          
        if "перевод_на_бюджет" in call.data:
            btns, text = text_editor.gen_form(content["Перевод на бюджет"],"FAQ_перевод_на_бюджет", call)  
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="FAQ")])
         
        
        if "dec" in call.data:
            btns.clear()
            btns.append( [InlineKeyboardButton(text="1", callback_data="FAQ_dec_1"), InlineKeyboardButton(text="2", callback_data="FAQ_dec_2"), InlineKeyboardButton(text="3", callback_data="FAQ_dec_3")])
            btns.append( [InlineKeyboardButton(text="4", callback_data="FAQ_dec_4"), InlineKeyboardButton(text="6", callback_data="FAQ_dec_6"), InlineKeyboardButton(text="8", callback_data="FAQ_dec_8")])
            btns.append( [InlineKeyboardButton(text="ФПТИ", callback_data="FAQ_dec_ФПТИ"), InlineKeyboardButton(text="12", callback_data="FAQ_dec_12")])
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="FAQ")])
            text =f"Выбирай нужный тебе"
            if "FAQ_dec_" in call.data:
                btns.clear()
                inst = call.data.split(sep="_")[-1]
                text = content[f"Деканат {inst}"]
                btns.append( [InlineKeyboardButton(text="Назад", callback_data="FAQ_dec")])

        if "FAQ_voenka" in call.data:
            btns, text = text_editor.gen_form(content["ВУЦ"], "FAQ_voenka", call)
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="FAQ")])

        if "FAQ_history" in call.data:
            btns, text = text_editor.gen_form(content["История ГУАП"],"FAQ_history", call )
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="FAQ")])
            bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open('castle.jpeg', "rb")))
        
    elif "answer_on_message" in call.data:
            
            try:
                questions = personal_asks.read_dict("personal_asks")
                id = call.data.split(sep = "_")[-1]
                
                for question in questions["questions"]:
                    if int(id) == int(question["id"]):
                        break
                
                if question["status"]=="answered":
                    bot.answer_callback_query(call.id, "На этот вопрос уже был получен ответ. Все отлично", show_alert=True)
                    
                else:
                    msg = bot.reply_to(call.message, 'Ответчаете')
                    bot.register_next_step_handler(msg, personal_asks.to_user, question["chat_id"], bot)
                
                    for question in questions["questions"]:
                        if int(id) == int(question["id"]):
                            question['status'] = "answered"
                            break
                    personal_asks.save_dict(questions, "personal_asks")
            except:
                bot.send_message(call.chat.id, f"Что-то пошло не так. username, чтобы ответить лично: {question['id']}")
            return
    
    
    if "refresh" in call.data:
         btns.append([InlineKeyboardButton(text="Сдал", callback_data=f"done_{call.data.split(sep='_')[1]}")])
         btns.append([InlineKeyboardButton(text="На новый круг", callback_data=f"ring_{call.data.split(sep='_')[1]}")])
         btns.append([InlineKeyboardButton(text="Просмотр Очереди", callback_data=f"refresh_{call.data.split(sep='_')[1]}")])
         gr = call.data.split(sep='_')[1]
         kd = InlineKeyboardMarkup(btns, row_width=2)
         text= server_con.get_queue(call.message.from_user.id, gr, call.message.from_user.username)
         text = json.loads(text)
         print (text)
         outp=""
         i=1
         for tex in text:
             outp+=str(i)+") @"+tex["userName"]+"\n"
             i+=1
         bot.answer_callback_query(call.id, text = outp, show_alert=True)
         return

    if "ring" in call.data:
        gr = call.data.split(sep='_')[1]
        server_con.del_user_from_queue(gr, call.from_user.id, call.from_user.username)
        server_con.add_user_to_queue(gr, call.from_user.id, call.from_user.username)
        bot.answer_callback_query( call.id, "Вы добавлены в конец очереди", show_alert= True)
        return
    
    if "done" in call.data:
        gr = call.data.split(sep='_')[1]
        server_con.del_user_from_queue(gr, call.from_user.id, call.from_user.username)
        bot.answer_callback_query( call.id, "Вы удалены из очереди", show_alert= True)
        return

    
    try:
        keyboard = InlineKeyboardMarkup(btns, row_width=2)
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,caption = text, reply_markup=keyboard)

    except :
        print("blaaaaaaa")
                
        keyboard = InlineKeyboardMarkup(btns, row_width=2)
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)  