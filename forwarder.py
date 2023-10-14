import json

def add_chat(username ,name, id):
    #add new forwarding
    with open("chats.json" , "r+" ) as file:
        file_data = json.load(file)
        
        chat = { "username": username,
                "chat_name": name,
                "chat_id": id}
        for item in file_data["chats"]:
            if item["chat_name"]==name or item["chat_id"]==id: 
                return None
        file_data['chats'].append(chat)
    with open("chats.json" , "w") as file:
        json.dump(file_data, file, indent=2, ensure_ascii=True)
    return chat

def get_id(chat_name):
    try:
        with open("chats.json" , "r+") as file:
            file_data = json.load(file)
            for chat in file_data["chats"]:
                if chat['chat_name']==chat_name:
                    return chat["chat_id"]
    except Exception:
        return None
    
def get_chat_name(chat_id):
    try:
        with open("chats.json" , "r+") as file:
            file_data = json.load(file)
            for chat in file_data["chats"]:
                if chat['chat_id']==chat_id:
                    return chat['chat_name']
    except Exception:
        return None


def get_all_chats():
     with open("chats.json" , "r+" , encoding='ascii') as file:
        file_data = json.load(file)
        return file_data
     

def change_chat_name(name,chat_id):
    try:
        with open("chats.json" , "r+") as file:
            
            file_data = json.load(file)
            for chat in file_data["chats"]:
                if chat['chat_id']==chat_id:
                    chat["chat_name"] = name.text
                    with open("chats.json" , "w") as file:
                        json.dump(file_data, file, indent=2, ensure_ascii=True)
                        return chat

    except Exception:
        return None
if __name__=="__main__":
    print() 