from Connect import *
import telethon.sync
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import asyncio

client=Connect.client()

tg_user='zaidibeth'

def sendMessage(username):
    try:
        client.send_message(username,'checking user')
        print('Message sent')
    except Exception as e:
        print('Exception details: ',e)

def getDialogs():
    get_dialogs = GetDialogsRequest(offset_date=None,offset_id=0,offset_peer=InputPeerEmpty(),limit=30,hash=0)
    dialogs = client(get_dialogs)
    return dialogs

def getUser(username):
    dialogs=getDialogs()
    for u in dialogs.users:
        print(u)
        if u.username.lower()==username.lower():
            print(u)
            print(u.id)
            print(u.username)
            return u
            #print(u.access_hash)
            #print(u.first_name)
            #print(u.last_name)
    else:
        print('User wasnt found in chats')

sendMessage(tg_user)
getUser(tg_user)