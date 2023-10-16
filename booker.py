import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import json
import text_editor
import texts
import personal_asks


def branch(call, bot):
    text = "Попробуй еще раз, что-то пошло не так (\n"
    content = text_editor.read_dict('texts')
    btns = []
    print(call.data)
    #начало ветвлений
    if "Bmenu" == call.data:
        btns.append( [InlineKeyboardButton(text="БСК", callback_data="Bbsk_0"), InlineKeyboardButton(text="Студсоветы", callback_data="Bstudsovet")]) 
        btns.append( [ InlineKeyboardButton(text="Промежуточная аттестация", callback_data="Bsession_0") , InlineKeyboardButton(text="Общаги", callback_data="Bhotels")])
        btns.append( [InlineKeyboardButton(text="Частозадаваемые", callback_data="BFAQ")])
        btns.append([InlineKeyboardButton(text="Свой вопрос", callback_data="Bpersonal_ask")])
        text = "Привет, я могу помочь тебе разобраться с тем, как все у нас в вузе устроено\n"
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(f"logo.jpeg", "rb")))

    if "Bbsk" in call.data:
        btns, text= text_editor.gen_form(content["БСК"], "Bbsk", call)
        btns.append([InlineKeyboardButton(text="Назад", callback_data="Bmenu")]) 
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(f"card.jpg", "rb")))
    if "Bpersonal_ask" in call.data:
            text = "Отправьте боту в чат команду /ask. Бот предложит вам задать ваш вопрос и передаст оператору. Ответ вы получите в этот чат."
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bmenu")])   

    elif "Bstudsovet" in call.data:
        text = "У каждого факультета в нашем вузе есть свой студсовет. Присоединяйся, ведь учиться вместе интересней. Ссылки на ВК ты можешь получить по кнопкам:"
        btns.append([InlineKeyboardButton("Общий студсовет ГУАП", url='https://vk.com/studsovguap')])
        btns.append([InlineKeyboardButton("Студсовет 1 Института", url='https://vk.com/guap_ssi_1'), InlineKeyboardButton("Студсовет 2 Института", url='https://vk.com/guap.ssi2')])
        btns.append([InlineKeyboardButton("Студсовет 3 Института", url='https://vk.com/studsovet_uyutno_3'), InlineKeyboardButton("Студсовет 4 Института", url='https://vk.com/guap_ss4')])
        btns.append([InlineKeyboardButton("Студсовет 6 Института", url='https://vk.com/shesterka_suai'), InlineKeyboardButton("Студсовет 8 Института", url="https://vk.com/guapstudsovet8")])
        btns.append([InlineKeyboardButton("Студсовет ФПТИ", url='https://vk.com/ssi_fpti'), InlineKeyboardButton("Студсовет 12 Института", url='https://vk.com/12fak')])
        btns.append([InlineKeyboardButton(text="Назад", callback_data="Bmenu")]) 
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(f"studsovet.jpeg", "rb")))
    elif "Bsession" in call.data:
        btns, text = text_editor.gen_form(content["Промежуточная аттестация"],"Bsession", call)
        btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bmenu")]) 
    

    
    elif "Bhotels" in call.data:
        btns.append( [InlineKeyboardButton(text="№1, пр. Маршала Жукова, д. 24", callback_data="Bhotels_№1")]) 
        btns.append( [InlineKeyboardButton(text="№2, ул. Передовиков, д. 13", callback_data="Bhotels_№2")]) 
        btns.append( [InlineKeyboardButton(text="№3, ул. Варшавская, д. 8", callback_data="Bhotels_№3")]) 
        btns.append( [InlineKeyboardButton(text="Вопросы", callback_data="Bhotels_faq")]) 
        btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bmenu")]) 
        text = "Всего у ГУАПа 3 общежития:"

        if "Bhotels_№"  in call.data:
            btns.clear()
            i = int(call.data[-1])
            text = texts.hotels[f"{i}"][0]
            btns.append( [InlineKeyboardButton(text="Группа в вк", url=texts.hotels[f"{i}"][1])]) 
            btns.append( [InlineKeyboardButton(text="Больше фоток", url=texts.hotels[f"{i}"][2])]) 
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bhotels")]) 
            bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open(texts.hotels[f"{i}"][3], "rb")))

        if "Bhotels_faq" == call.data:
            btns.clear()
            text = texts.hotels["faq"][0]
            btns.append( [InlineKeyboardButton(text="1/2 >>", callback_data="Bhotels_faq_1")]) 
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bhotels")]) 
        if "Bhotels_faq_1" == call.data:
            btns.clear()
            text = texts.hotels["faq"][1]
            btns.append( [InlineKeyboardButton(text="2/2 <<", callback_data="Bhotels_faq")]) 
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bhotels")]) 
    
    elif "BFAQ" in call.data:
        btns.append( [InlineKeyboardButton(text="Контакты деканатов", callback_data="BFAQ_dec") ,InlineKeyboardButton(text="Военная кафедра", callback_data="FAQ_voenka_0")]) 
        btns.append( [InlineKeyboardButton(text="Про стипендию", callback_data="BFAQ_stipendiya_0"), InlineKeyboardButton(text="История ГУАП", callback_data="FAQ_history_0")])
        btns.append( [InlineKeyboardButton(text="Перевод на бюджет", callback_data="BFAQ_перевод_на_бюджет_0")])  
        btns.append( [InlineKeyboardButton(text="Назад", callback_data="Bmenu")]) 
    
        text = "Раздел FAQ"

        if "Bstipendiya" in call.data:
            btns, text = text_editor.gen_form(content["Стипендия"], "BFAQ_stipendiya", call)
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="BFAQ")])
          
        if "Bперевод_на_бюджет" in call.data:
            btns, text = text_editor.gen_form(content["Перевод на бюджет"],"BFAQ_перевод_на_бюджет", call)  
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="BFAQ")])
         
        
        if "Bdec" in call.data:
            btns.clear()
            btns.append( [InlineKeyboardButton(text="1", callback_data="BFAQ_dec_1"), InlineKeyboardButton(text="2", callback_data="FAQ_dec_2"), InlineKeyboardButton(text="3", callback_data="FAQ_dec_3")])
            btns.append( [InlineKeyboardButton(text="4", callback_data="BFAQ_dec_4"), InlineKeyboardButton(text="6", callback_data="FAQ_dec_6"), InlineKeyboardButton(text="8", callback_data="FAQ_dec_8")])
            btns.append( [InlineKeyboardButton(text="ФПТИ", callback_data="BFAQ_dec_ФПТИ"), InlineKeyboardButton(text="12", callback_data="FAQ_dec_12")])
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="BFAQ")])
            text =f"Выбирай нужный тебе"
            if "FAQ_dec_" in call.data:
                btns.clear()
                inst = call.data.split(sep="_")[-1]
                text = content[f"Деканат {inst}"]
                btns.append( [InlineKeyboardButton(text="Назад", callback_data="BFAQ_dec")])

        if "BFAQ_voenka" in call.data:
            btns, text = text_editor.gen_form(content["ВУЦ"], "BFAQ_voenka", call)
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="BFAQ")])

        if "BFAQ_history" in call.data:
            btns, text = text_editor.gen_form(content["История ГУАП"],"BFAQ_history", call )
            btns.append( [InlineKeyboardButton(text="Назад", callback_data="BFAQ")])
            bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           media=InputMedia(type='photo', media=open('castle.jpeg', "rb")))
        
    elif "Banswer_on_message" in call.data:
            
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
    
    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,caption = text, reply_markup=keyboard)
    