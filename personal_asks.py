import json
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton



def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

def read_dict(name):
    with open(str(name) + '.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data


def get_question(message, bot):
    print(message.text)
    try: 
        questions = read_dict("personal_asks")
        
        question = {'date': str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), 'text':message.text, 'user': message.from_user.username, 'chat_id': message.chat.id, 'id': len(questions["questions"]), 'status': "in process"}
        questions['questions'].append(question)
        save_dict(questions, "personal_asks")
       
        redirected_message = f"Поступил новый вопрос в {question['date']} от @{question['user']}:\n {question['text']}"
        answ_btn = InlineKeyboardButton(text="Дать ответ", callback_data=f"answer_on_message_{question['id']}")
        keyboard = InlineKeyboardMarkup( row_width=2)
        keyboard.add(answ_btn)
        operators = read_dict("FAQ_Crew")
        
        for operator in operators["Crew"]:
            bot.send_message(operator["id"], text = redirected_message, reply_markup = keyboard)
        print(1)
        bot.send_message(message.chat.id, text = "Ваш вопрос передан оператору. Ожидайте ответа")
    except:
        bot.send_message(message.chat.id, text = "Что-то пошло не так. Попробуйте еще раз")



def remove_operator(message, bot):
    q = read_dict("FAQ_Crew")
  
    for item in q["Crew"]:
        if message.chat.id == item["id"]:
            q["Crew"].remove(item)

    save_dict(q, "FAQ_Crew")
    bot.send_message(message.chat.id, f"Вы Удалены из списка операторов")  

def add_operator(message, bot):
    q = read_dict("FAQ_Crew")
    user = {"id": message.chat.id, "username": message.from_user.username}
    q['Crew'].append(user)
    save_dict(q, "FAQ_Crew")
    bot.send_message(message.chat.id, f"Вы добавлены в список операторов. Ваш чат id с ботом: {message.chat.id}")  

def to_user(message, id, bot):
   bot.send_message(id, message.text)  

#if __name__=="__main__":
    