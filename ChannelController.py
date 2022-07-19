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

    def sendMessage(self, client, username):
        try:
            client.send_message(username,'checking user')
            print('Message sent')
        except Exception as e:
            print('Exception details: ',e)

    def getDialogs(self, client):
        get_dialogs = GetDialogsRequest(offset_date=None,offset_id=0,offset_peer=InputPeerEmpty(),limit=30,hash=0)
        dialogs = client(get_dialogs)
        return dialogs

    def getUser(self, username, client):
        dialogs=self.getDialogs(client)
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

    def saveUser(self, username, id, file='users/users'):
        found=False
        with open(file+'.txt') as f:
            if str(id) in f.read():
                found=True
            f.close()
        if not found:
            #f = open(file+".txt", 'a', encoding='utf-8')
            f = open(file+".txt", 'a', encoding='utf-8')
            f.write(str(id) + " " + username + "\n")
            f.close()
        else:
            print("User " + username + " is already in the file")
    
    def recoverUsers(self,file='users/users'):
        f = open(file+".txt",'r',encoding = 'utf-8')
        for line in f:
            print(line)
            data=line.split(" ")
            self.users[int(data[0])]=data[1]
            print("User "+ data[1] +" was succesfully recovered")
        f.close()

    def storeUsers(self, ids, usernames, file='users/users'):
        for i in range(len(ids)):
            self.users[ids[i]]=usernames[i]
            f = open(file+".txt", 'a', encoding='utf-8')
            f.write(str(ids[i]) + " " + usernames[i] + "\n")
            f.close()
    
    async def storeUser(self, client, channel, username, file='users/users'):
        id = await self.getUserID(client, channel, username)
        if type(id) != NoneType:
            self.users[id]=username
            self.saveUser(username, id, file)
            print("User successfully assigned and saved")
        else:
            print("Cannot store user " + username + " because it wasn't found")
            '''
            print("Let's try again")
            self.sendMessage(client, username)
            found=self.getUser(username,client)
            if type(found) != NoneType:
                self.users[found.id]=username
                self.saveUser(username, id, file)
                print("User successfully assigned and saved")
            else:
                print('Second try failed. Let it go.')
            '''


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

    async def getHistory(self, channel_id, client):
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
                history = await client(GetHistoryRequest(peer=my_channel,offset_id=offset_id,offset_date=None,add_offset=0,limit=limit,max_id=0,min_id=0,hash=0))    
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
        df_chatters = self.filterPerUsers(chatters_ids,df)
        self.dataframes.append(df_chatters)


    def filterPerUsers(self, chatters_ids,df):
        df_chatters = df[df.sender.isin(chatters_ids)]
        df_chatters.head()
        df_chatters['sender'] = df['sender'].map(self.users,na_action=None)
        return df_chatters

    def filterPerDate(self, eldest, newest, df):
        #df.loc['01/05/2022':'31/05/2022']
        df=df.loc[eldest:newest]
        return df

    def getDataframes(self):
        return self.dataframes

    def printStats(self, dataframes, doc_name):
        df = pd.concat(dataframes, axis=0)
        now=datetime.datetime.now()
        df.to_csv("stats/" + doc_name + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + '.csv', index=False,header=True)
        print('File ' + "stats/" + doc_name + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + ' created succesfully')

    async def sleep(self, delay):
        await asyncio.sleep(delay)


    async def main(self, channel_id,client):
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
                hash=0))    
            except Exception as e:
                print ("Exception details: ",e)
                await asyncio.sleep(10)
                continue
            if not history.messages:
                break
            for message in history.messages:
                date=message.date.replace(tzinfo=None)
                date_compare=datetime.datetime(2022, 7, 1).replace(tzinfo=None)
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
            date_compare=datetime.datetime(2022, 7, 1).replace(tzinfo=None)
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
        df_chatters = self.filterPerUsers(chatters_ids,df)
        #df_chatters=self.filterPerDate('01/05/2022','31/05/2022', df_chatters)
        self.dataframes.append(df_chatters)
        #now=datetime.datetime.now()
        #df_chatters.to_csv("stats/" + my_channel.title + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + '.csv', index=False,header=True)
        #print('File ' + "stats/" + my_channel.title + "-" + now.strftime(r'%d-%m-%Y-%H-%S-%M') + ' created succesfully')


'''def reportRegularProjects():
    projects_ids = [1377587241, 1125567813, 1473496284, 1598082994, 1775645809] #SNE, REBL, Rango, Stepn, Prop
    #projects_titles = ['StrongNode Edge','REBASE GG - OFFICIAL (CHAT)', 'Rango','STEPN Official English Group ♾', 'PropChain - Community']
    #projects_names=['strongnodechat','REBASE_gg','rangoexchange','Wavescommunity', 'STEPNofficialex'] #Propchain isn't here
    chatters=['zergcore','Kim_1415', 'monkeylegionn', 'ivelosthopes', 'cryptoojamess', 'Longjyckle', 'gabygab_01', 'lightyagami2nd', 'annalissamlh', 'stitchbby', 'traderattempt', 'sttevewithTT', 'strawberrychann', 'muhfree57', 'captionerkk877', 'Pronx1', 'Greensoldier', 'itsjerkinsnotjerking', 'notanonion', 'lithooman58', 'fragger98', 'Saint1v', 'alejandraa', 'Melisassd', 'ericsims1', 'bonny377', 'jtrapiello', 'thebigched', 'cjone00', 'eduardanchang', 'Daddygod20', 'Bigboss30', 'dian377', 'jackbitcoin', 'thehugoneitor', 'Anwua4', 'Furbee123', 'Mynameisdogo', 'NicolloMo', 'LucazzZ123', 'CapitanCrunch12', 'uadondawest', 'Japan213', 'yungburrito2', 'cinnarolls9', 'mjape20', 'alvin365', 'Harry209', 'Heavyweight2', 'km2k15']

    client=Connect.client()
    ch=ChannelController()
    dialogs=ch.getDialogs(client)
    ch.storeChats(dialogs)
    ch.storeChannels(dialogs,projects_ids)
    #ch.storeUsers(wolf_ids,wolf)
    for user in chatters:
        with client:
            client.loop.run_until_complete(ch.storeUser(client,'strongnodechat',user))
    ch.recoverUsers()
    for chnn in ch.channels:
        with client:
            client.loop.run_until_complete(ch.main(client, chnn.id))
    ch.printStats(ch.getDataframes(),'Regular')        

reportRegularProjects()
'''

def reportFullWavesProjects():
    """
    Document shit
    """
    projects_ids=[1112416724,1173560544,1446148003,1225614362] #Waves, Vires, WavesExchange, Neutrino Ids
    daily=sara+alejandra+hugo+josue+karla
    sara=['Kim_1415', 'monkeylegionn', 'ivelosthopes', 'cryptoojamess', 'Longjyckle', 'gabygab_01', 'lightyagami2nd', 'annalissamlh', 'stitchbby', 'traderattempt', 'sttevewithTT', 'strawberrychann']
    alejandra=['muhfree57', 'captionerkk877', 'Pronx1', 'Greensoldier', 'itsjerkinsnotjerking', 'notanonion', 'lithooman58', 'fragger98', 'Saint1v', 'alejandraa', 'Melisassd']
    hugo=['ericsims1', 'bonny377', 'jtrapiello', 'thebigched', 'cjone00', 'eduardanchang', 'Daddygod20', 'Bigboss30', 'dian377', 'jackbitcoin', 'thehugoneitor']
    josue=['Anwua4', 'Furbee123', 'Mynameisdogo', 'NicolloMo', 'LucazzZ123', 'CapitanCrunch12', 'uadondawest', 'Japan213', 'yungburrito2']
    karla=['cinnarolls9', 'mjape20', 'alvin365', 'Harry209', 'Heavyweight2', 'km2k15']
    wolf=['kmsnowpls','NutiusMaximus', 'Mrfrogman00', 'fucktheteutonic', 'pleasestopthepain']
    saint=['artoriasfirstsign','AlPastor00','depravedmonolith','GateKeeppp','richgoldbergSon']
    username=['feelingsomthing', 'ancapenjoyer','firepunch1','nopegineerr','NosferatuAlucard']
    anti_fud=wolf+saint+username
    all=daily

    client=Connect.client()
    ch=ChannelController()
    dialogs=ch.getDialogs(client)
    ch.storeChats(dialogs)
    ch.storeChannels(dialogs,projects_ids)
    for user in all:
        with client:
            client.loop.run_until_complete(ch.storeUser(client,'Wavescommunity',user,'users/all'))
    #ch.recoverUsers()
    for chnn in ch.channels:
        with client:
            client.loop.run_until_complete(ch.main(chnn.id, client))
    ch.printStats(ch.getDataframes(),'Waves-daily')

reportFullWavesProjects()