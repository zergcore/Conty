from tkinter import E
from types import NoneType
import telethon.sync
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import PeerUser
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from Connect import *
import pandas as pd
import asyncio
import json
import datetime
import pytz as tz

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

class ChannelController:

    def __init__(self):
        pass

    def __init__(self) -> None:
        # create dictionary of ids to users and chats
        self.users={}
        self.chats={}
        self.channels=[]
        self.dataframes=[]

    def getDialogs(self, client):
        get_dialogs = GetDialogsRequest(offset_date=None,offset_id=0,offset_peer=InputPeerEmpty(),limit=30,hash=0)
        dialogs = client(get_dialogs)
        return dialogs

    async def getUserID(self, client, channel, username):
        participants = await client(GetParticipantsRequest(channel, ChannelParticipantsSearch(username), 0, 200, 0))
        u=participants.users
        if len(u)>0:
            print(u[0])
        await asyncio.sleep(5)
        try:
            user_id=participants.users[0].id
            print("User " + username +" succesfully found, id: " + str(user_id))
            return user_id
        except Exception as e:
            print("Error details: ", e)
            print("User " + username + " not found in " + channel)
            return

    def saveUser(self, username, id):
        found=False
        with open('users_waves.txt') as f:
            if str(id) in f.read():
                found=True
            f.close()
        if not found:
            #f = open("users_waves.txt", 'a', encoding='utf-8')
            f = open("users_waves.txt", 'a', encoding='utf-8')
            f.write(str(id) + " " + username + "\n")
            f.close()
        else:
            print("User " + username + " is already in the file")
    
    def recoverUsers(self):
        file = open("users_waves.txt",'r',encoding = 'utf-8')
        for line in file:
            print(line)
            data=line.split(" ")
            self.users[int(data[0])]=data[1]
            print("User "+ data[1] +" was succesfully recovered")
        file.close()

    def storeUsers(self, ids, usernames):
        for i in range(len(ids)):
            self.users[ids[i]]=usernames[i]
            f = open("users_waves.txt", 'a', encoding='utf-8')
            f.write(str(ids[i]) + " " + usernames[i] + "\n")
            f.close()
    
    async def storeUser(self, client, channel, username):
        id = await self.getUserID(client, channel, username)
        if type(id) != NoneType:
            self.users[id]=username
            self.saveUser(username, id)
            print("User successfully assigned and saved")
        else:
            print("Cannot store user " + username + " because it wasn't found")

    def storeChats(self,dialogs):
        for c in dialogs.chats:
            self.chats[c.id] = c

    def storeChannels(self, dialogs, projects_ids):
        for d in dialogs.dialogs:
            peer = d.peer
            if isinstance(peer, PeerChannel):
                id = peer.channel_id
                channel = self.chats[id]
                if channel.id in projects_ids:
                    self.channels.append(channel)
                    '''access_hash = channel.access_hash
                    name = channel.title
                    input_peer = InputPeerChannel(id, access_hash)
                    input_channel = InputChannel(id, access_hash)'''
                    #print("channel access_hash")
                    #print(name + ":" + str(access_hash))
                else:
                    continue
            else:
                continue

    def getDate(self, date_object):
        date = tz.utc.localize(date_object)
        date_est=date.astimezone(tz.timezone('America/New_York'))
        date_time = date_est.strftime("%d/%m/%Y %H:%M:%S")
        return date_time

    def getMessages(self, client, input_channel, limit):
        messages = client.get_messages(input_channel, limit)
        #await asyncio.sleep(limit/100)
        message_id =[]
        message =[]
        sender =[]
        time = []
        if len(messages):
            for chat in messages:
                u = chat.from_id
                if isinstance(u, PeerUser):
                    message_id.append(chat.id)
                    message.append(chat.message)
                    sender.append(u.user_id)
                    time.append(chat.date)

        data ={'message_id':message_id, 'message': message, 'sender':sender, 'time':time}
        df = pd.DataFrame(data)
        return df

    def getHistory(self, client, input_peer):
        message_id =[]
        message =[]
        sender =[]
        time = []
        get_history = GetHistoryRequest(
            peer=input_peer,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=1,
            max_id=0,
            min_id=0,
            hash=0,
        )
        history = client(get_history)
        if len(history.messages):
            for chat in history.messages:
                u = chat.from_id
                if isinstance(u, PeerUser):
                    message_id.append(chat.id)
                    message.append(chat.message)
                    sender.append(u.user_id)
                    time.append(chat.date)
        data ={'message_id':message_id, 'message': message, 'sender':sender, 'time':time}
        df = pd.DataFrame(data)
        return df

    def filterData(self, chatters_ids,df):
        df_chatters = df[df.sender.isin(chatters_ids)]
        df_chatters.head()
        df_chatters['sender'] = df['sender'].map(self.users,na_action=None)
        return df_chatters

    def getDataframes(self):
        return self.dataframes

    def printStats(self, dataframes, doc_name):
        df = pd.concat(dataframes, axis=0)
        now=datetime.datetime.now()
        df.to_csv(doc_name + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + '.csv', index=False,header=True)
        print('File ' + doc_name + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + ' created succesfully')

    async def sleep(self, delay):
        await asyncio.sleep(delay)


    async def main(self, channel_id):
        await client.start()

        my_channel = await client.get_entity(PeerChannel(int(channel_id)))
        print(my_channel.title)

        offset_id = 0
        limit = 100
        messages = []
        message_id = []
        sender =[]
        timestamp =[]
        total_messages = 0
        total_count_limit = 0
        date=datetime.datetime.now().replace(tzinfo=None)

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            try:
                history = await client(GetHistoryRequest(peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
                ))    
            except Exception as e:
                print ("Exception details: ",e)
                await asyncio.sleep(10)
                continue
            if not history.messages:
                break
            for message in history.messages:
                date=message.date.replace(tzinfo=None)
                date_compare=datetime.datetime(2022, 6, 1).replace(tzinfo=None)
                if date<date_compare:
                    break
                u = message.from_id
                if not isinstance(u, PeerUser):
                    break
                try:
                    message_id.append('https://t.me/'+my_channel.username+'/'+str(message.id))
                except Exception as e:
                    print("Exception details: ", e)
                    message_id.append('https://t.me/'+str(channel_id)+'/'+str(message.id))
                messages.append(message.message)
                sender.append(u.user_id)
                timestamp.append(self.getDate(message.date.replace(tzinfo=None)))
            date_compare=datetime.datetime(2022, 6, 1).replace(tzinfo=None)
            if date<date_compare:
                break
            offset_id = history.messages[len(history.messages) - 1].id
            total_messages = len(messages)
            total_count_limit=history.count
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        dt ={'message': messages, 'sender':sender, 'link':message_id, 'time':timestamp, 'channel':my_channel.title}
        df = pd.DataFrame(dt)
        # disable chained assignments
        pd.options.mode.chained_assignment = None 
        chatters_ids=list(self.users.keys())
        df_chatters = self.filterData(chatters_ids,df)
        self.dataframes.append(df_chatters)
        #now=datetime.datetime.now()
        #df_chatters.to_csv(my_channel.title + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + '.csv', index=False,header=True)
        #print('File ' + my_channel.title + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + ' created succesfully')


#projects_titles = ['StrongNode Edge','REBASE GG - OFFICIAL (CHAT)', 'Rango','STEPN Official English Group ♾', 'PropChain - Community']
#projects_ids = [1377587241, 1125567813, 1473496284, 1598082994, 1775645809] #SNE, REBL, Rango, Stepn, Prop
#projects_names=['strongnodechat','REBASE_gg','rangoexchange','Wavescommunity', 'STEPNofficialex'] #Propchain isn't here
#chatters_ids=[1157661659,259666186,1730962980,1779713175,1350200586]


projects_ids=[1112416724,1173560544,1446148003,1225614362] #Waves, Vires, WavesExchange, Neutrino Ids
wolf_ids=[1646032571,1783689378,1455185808,1664917820,1643813244] #WolfIDs
wolf_usernames=['kmsnowpls','NutiusMaximus', 'Mrfrogman00', 'fucktheteutonic', 'pleasestopthepain']
chatters_usernames=['artoriasfirstsign','AlPastor00','depravedmonolith','GateKeeppp','richgoldbergSon', 'feelingsomthing', 'ancapenjoyer'] #Saint and Username users
#chatters_usernames=['zergcore','Kim_1415', 'monkeylegionn', 'ivelosthopes', 'cryptoojamess', 'Longjyckle', 'gabygab_01', 'lightyagami2nd', 'annalissamlh', 'stitchbby', 'traderattempt', 'sttevewithTT', 'strawberrychann', 'muhfree57', 'captionerkk877', 'Pronx1', 'Greensoldier', 'itsjerkinsnotjerking', 'notanonion', 'lithooman58', 'fragger98', 'Saint1v', 'alejandraa', 'Melisassd', 'ericsims1', 'bonny377', 'jtrapiello', 'thebigched', 'cjone00', 'eduardanchang', 'Daddygod20', 'Bigboss30', 'dian377', 'jackbitcoin', 'thehugoneitor', 'Anwua4', 'Furbee123', 'Mynameisdogo', 'NicolloMo', 'LucazzZ123', 'CapitanCrunch12', 'uadondawest', 'Japan213', 'yungburrito2', 'cinnarolls9', 'mjape20', 'alvin365', 'Harry209', 'Heavyweight2', 'km2k15']

client=Connect.client()
ch=ChannelController()
dialogs=ch.getDialogs(client)
ch.storeChats(dialogs)
ch.storeChannels(dialogs,projects_ids)
ch.storeUsers(wolf_ids,wolf_usernames)
for user in chatters_usernames:
    with client:
        client.loop.run_until_complete(ch.storeUser(client,'Wavescommunity',user))
ch.recoverUsers()
for chnn in ch.channels:
    with client:
        client.loop.run_until_complete(ch.main(chnn.id))
        #print(">> Cancelling tasks now")
        #for task in asyncio.Task(client):
            #task.cancel()
        #print(">> Done cancelling tasks")
        #asyncio.get_event_loop().stop()
        #client.loop.run_until_complete(ch.sleep(30))
ch.printStats(ch.getDataframes(),'Waves')


'''data=ch.getHistory(client, InputPeerChannel(chnn.id, chnn.access_hash))
    print(data)'''
'''try:
        data=asyncio.run(ch.getMessages(client,InputChannel(chnn.id, chnn.access_hash),500))
        print(chnn.title)
        print(data)
    except Exception as e:
        print(e)'''
        

    

'''    get_history = GetHistoryRequest(
        peer=input_peer,
        offset_id=0,
        offset_date=None,
        add_offset=0,
        limit=1,
        max_id=0,
        min_id=0,
        hash=0,
    )

    history = client(get_history)
    if isinstance(history, Messages):
        count = len(history.messages)
    else:
        count = history.count
        u=history.users

    counts[name] = count
    users[name]=u

print("sorted_counts")
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
for name, count in sorted_counts:
    print('{}: {}'.format(name, count))

'''