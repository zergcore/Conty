from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import pandas as pd
from connect import *
import telethon.sync
import asyncio
from telethon.tl.types import InputChannel

client=Connect.client()

usernames=['Kim_1415', 'monkeylegionn', 'ivelosthopes', 'cryptoojamess', 'Longjyckle', 'gabygab_01', 'lightyagami2nd', 'annalissamlh', 'stitchbby', 'traderattempt', 'sttevewithTT', 'strawberrychann', 'muhfree57', 'captionerkk877', 'Pronx1', 'Greensoldier', 'itsjerkinsnotjerking', 'notanonion', 'lithooman58', 'fragger98', 'Saint1v', 'alejandraa', 'Melisassd', 'ericsims1', 'bonny377', 'jtrapiello', 'thebigched', 'cjone00', 'eduardanchang', 'Daddygod20', 'Bigboss30', 'dian377', 'jackbitcoin', 'thehugoneitor', 'cinnarolls9', 'mjape20', 'alvin365', 'Harry209', 'Heavyweight2']

projects_titles = ['StrongNode Edge','REBASE GG - OFFICIAL (CHAT)','Waves Official 🌊 (1 ➝ 2)','STEPN Official English Group ♾', 'PropChain - Community']
projects_ids = [1377587241, 1125567813, 1112416724, 1598082994, 1775645809]
projects_names=['strongnodechat','REBASE_gg', 'Wavescommunity', 'STEPNofficialex']
waves_names=['Wavescommunity']
waves_ids=[1112416724]

firstname =[]
lastname = []
username = []
ids=[]

'''chatters_usernames=['artoriasfirstsign','AlPastor00','depravedmonolith','GateKeeppp','richgoldbergSon', 'feelingsomthing', 
'ancapenjoyer', 'firepunch1','nopegineerr','NosferatuAlucard']'''

participants = client(GetParticipantsRequest('Wavescommunity', ChannelParticipantsSearch('NosferatuAlucard'), 0, 200, 0))
#InputChannel can also be a string of the name of the group, but as this group is private, we use InputChannel with the ID and access_hash

#channels.getParticipants#123e05e9 channel:InputChannel filter:ChannelParticipantsFilter offset:int limit:int hash:int = channels.ChannelParticipants

for user in participants.users:
    print(type(user))
    print(user.stringify())
    firstname.append(user.first_name)
    lastname.append(user.last_name)
    username.append(user.username)
    ids.append(user.id)

data ={'ids':ids,'first_name' :firstname, 'user_name':username}
userdetails = pd.DataFrame(data)

print(userdetails)