import requests
import json

path = "https://a018-194-226-199-236.ngrok-free.app"

def get_all_users_in_group(user_id, group_name):
    headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
    }

    json_data = {
        'userId': user_id,
        'groupName': group_name,
    }

    response = requests.post(
        f'{path}/api/User/GetAllUsersByGroupKey',
        headers=headers,
        json=json_data,
    )
    return json.loads(response.text)

def create_queue(user_id, g_name, username):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'uniqId': g_name,
        'user': {
            'userId': user_id,
            'userName': username,
        },
    }

    response = requests.post(  f'{path}/api/Queue/CreateQueue', headers=headers, json=json_data)
    

def get_queue(user_id, g_name, username):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = { 
        'uniqId': g_name,
        'user': {
            'userId': user_id,
            'userName': username,
        },
    }
    response = requests.post(  f'{path}/api/Queue/GetQueue', headers=headers, json=json_data)
    return response.text

def get_users_groups(user_id, username):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'userId': user_id,
        'userName': username,
    }

    response = requests.post(
        f'{path}/api/User/GetAllGroupsByUserId',
        headers=headers,
        json=json_data,
    )

    return json.loads(response.text)

def add_user_to_queue(group, user_id, username):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
       'uniqId': group,
        'user': {
            'userId': user_id,
            'userName': username,
        },
    }

    response = requests.post(  f'{path}/api/Queue/AddInQueue', headers=headers, json=json_data)


def del_user_from_queue(group, user_id, username):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'uniqId': group,
        'user': {
            'userId': user_id,
            'userName': username,
        },
    }

    response = requests.post(
        f'{path}/api/Queue/DeleteFromQueue',
        headers=headers,
        json=json_data,
    )

def add_message(group, id):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'uniqId': group,
        'messageRef': id
    }

    response = requests.post(  f'{path}/api/Queue/SetMessage', headers=headers, json=json_data)


def get_messages_id(group, user_id, username):
    headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
    }

    json_data = {
        'uniqId': group,
        'user': {
            'userId': user_id,
            'userName': username,
        },
    }
    response = requests.post(  f'{path}/api/Queue/GetMessages', headers=headers, json=json_data)
    return json.loads(response.text)['messageRef']


def create_group(g_name, user_id, username):

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'userId': user_id,
        'groupName': g_name.text,
        'userName': username
    }

    response = requests.post('https://a018-194-226-199-236.ngrok-free.app/api/Group/CreateGroup', headers=headers, json=json_data)

def join_group(g_name, user_id, username):
        
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
         'userId': user_id,
        'groupName': g_name.text,
        'userName': username
    }

    response = requests.post('https://a018-194-226-199-236.ngrok-free.app/api/Group/ConnectToGroup', headers=headers, json=json_data)


if __name__=="__main__":
    #print(add_user_to_queue("4134", 637382945, "Ewokasi"))
    print(get_all_users_in_group(user_id=637382945, group_name="4134"))