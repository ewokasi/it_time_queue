from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
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