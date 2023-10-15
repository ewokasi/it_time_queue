from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
import forwarder
import telebot
import server_con
import json

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


    ###################################firewall#############################
    if "fw_settings"in call.data:
        fw =[]
        fw.append([InlineKeyboardButton(text="Ваше Имя", callback_data="red_name")])
        fw.append([InlineKeyboardButton(text="Посмотреть все чаты", callback_data="all_chats")])
        fw.append([InlineKeyboardButton(text="Гайд", callback_data="fw_guide")])
        fw_kb = InlineKeyboardMarkup(fw, row_width=1)
        bot.edit_message_text(chat_id= call.message.chat.id, message_id= call.message.id,text = """Настойки файрволла. 
    -Поменяйте Имя, которым будет подписано ваше сообщение
    -Просмотр всех чатов, которым вы можете отправить сообщение
    -Как указать чат по умолчанию для входящих
    -Гайд по использованию файрволла для связи""", reply_markup=fw_kb)
        return

    if "red_name" in call.data:
        name_info=f"""Сейчас все, кому вы отправляете сообщение из этого чата видят вас как {forwarder.get_chat_name(call.message.chat.id)}
Вы можете изменить предпочитаемое имя по кнопке ниже"""
        bt= []
        bt.append([InlineKeyboardButton(text="Поменять имя", callback_data="change_chat_name")])
        bt.append([InlineKeyboardButton(text="Назад", callback_data="fw_settings")])
        kb=InlineKeyboardMarkup(bt)
        bot.edit_message_text(chat_id= call.message.chat.id, message_id= call.message.id, text = name_info, reply_markup= kb)

        return
    if "change_chat_name" in call.data:
        msg = bot.send_message(call.message.chat.id, "Введите новое имя для этого чата. Если вы передумали, введите свое прошлое название чата")
        bot.register_next_step_handler(msg, forwarder.change_chat_name, call.message.chat.id ) 
        return
    
    if "all_chats" in call.data:
        outp= ""
        chats = forwarder.get_all_chats()
        for chat in chats["chats"]:
            outp+= chat["chat_name"]+"\n"
        bot.send_message(call.message.chat.id, outp)
        return
        
    if "fw_guide" in call.data:
        outp= "Чтобы отправить сообщение напишите получателя с тегом @\n Например: @Староста 4134, Я задержусь"
        bot.send_message(call.message.chat.id, outp)
        return
 ###################################firewall#############################
    text = "Попробуй еще раз, что-то пошло не так (\n"
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

    

    keyboard = InlineKeyboardMarkup(btns, row_width=2)
    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)