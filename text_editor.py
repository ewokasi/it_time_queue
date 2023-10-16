import json
import texts
import docx
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_form(multistring, name, call):
    pages = len(multistring)
    print("pages:",pages)
    btns=[]
    if name in call.data:
            btns.clear()
            if call.data==f"{name}_0":
                i = 0
            else:
                i = int(call.data.split(sep="_")[-1])

            if i !=0  and i!=pages-1:
                btns.append( [InlineKeyboardButton(text=f"{i}/{pages} <<", callback_data=f"{name}_{i-1}") ,InlineKeyboardButton(text=f">> {i+2}/{pages}", callback_data=f"{name}_{i+1}")])
            elif i ==0:
                btns.append( [InlineKeyboardButton(text=f" >> {i+1}/{pages}", callback_data=f"{name}_{i+1}")])
            elif i==pages-1:
                 btns.append( [InlineKeyboardButton(text=f"{i}/{pages} <<", callback_data=f"{name}_{i-1}")])
    print("i",i)
    text = multistring[i]
    print("text", text)
    return btns , text


def getText(filename):
    doc = docx.Document(filename)
    fullText = ""
   
    for para in doc.paragraphs:
        fullText+= para.text+' '
    
    return fullText

def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

def read_dict(name):
    with open(str(name) + '.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data


def separate_text(multistring):
    separated_strings = []
    i = 0
    string = ""
    for i in range(len(multistring)):
        string+=multistring[i]
        if i%1000==0 and i!=0:
            separated_strings.append(string)
            string=""
    separated_strings.append(string)
    
    return separated_strings


def update_text(name, multistring):
    content = separate_text(multistring)
    print("---------------content---------------",content)
    text = read_dict("texts")
    text[f"{name}"] = content
    save_dict(text, "texts")

if __name__ =="__main__":
    update_text("bla", "blafdgfdgdfgfdbla")