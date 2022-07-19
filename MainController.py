from ChannelController import *
from Connect import *

def reportRegularProjects():
    """
    Document shit
    """
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
    '''for user in chatters:
        with client:
            client.loop.run_until_complete(ch.storeUser(client,'strongnodechat',user))
    '''
    ch.recoverUsers()
    for chnn in ch.channels:
        with client:
            client.loop.run_until_complete(ch.main(chnn.id, client))
    ch.printStats(ch.getDataframes(),'Regular')     

def reportFullWavesProjects():
    """
    Document shit
    """
    projects_ids=[1112416724,1173560544,1446148003,1225614362] #Waves, Vires, WavesExchange, Neutrino Ids
    daily=['Kim_1415', 'monkeylegionn', 'ivelosthopes', 'cryptoojamess', 'Longjyckle', 'gabygab_01', 'lightyagami2nd', 'annalissamlh', 'stitchbby', 'traderattempt', 'sttevewithTT', 'strawberrychann', 'muhfree57', 'captionerkk877', 'Pronx1', 'Greensoldier', 'itsjerkinsnotjerking', 'notanonion', 'lithooman58', 'fragger98', 'Saint1v', 'alejandraa', 'Melisassd', 'ericsims1', 'bonny377', 'jtrapiello', 'thebigched', 'cjone00', 'eduardanchang', 'Daddygod20', 'Bigboss30', 'dian377', 'jackbitcoin', 'thehugoneitor', 'Anwua4', 'Furbee123', 'Mynameisdogo', 'NicolloMo', 'LucazzZ123', 'CapitanCrunch12', 'uadondawest', 'Japan213', 'yungburrito2', 'cinnarolls9', 'mjape20', 'alvin365', 'Harry209', 'Heavyweight2', 'km2k15']
    wolf=['kmsnowpls','NutiusMaximus', 'Mrfrogman00', 'fucktheteutonic', 'pleasestopthepain']
    saint=['artoriasfirstsign','AlPastor00','depravedmonolith','GateKeeppp','richgoldbergSon']
    username=['feelingsomthing', 'ancapenjoyer','firepunch1','nopegineerr','NosferatuAlucard']
    anti_fud=wolf+saint+username
    all=anti_fud+daily

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
    ch.printStats(ch.getDataframes(),'Waves')

#reportRegularProjects()
reportFullWavesProjects()

'''projects_ids=[1112416724,1173560544,1446148003,1225614362] #Waves, Vires, WavesExchange, Neutrino Ids
wolf_ids=[1646032571,1783689378,1455185808,1664917820,1643813244]
wolf=['kmsnowpls','NutiusMaximus', 'Mrfrogman00', 'fucktheteutonic', 'pleasestopthepain']
saint=['artoriasfirstsign','AlPastor00','depravedmonolith','GateKeeppp','richgoldbergSon']
username=['feelingsomthing', 'ancapenjoyer','firepunch1','nopegineerr','NosferatuAlucard']
anti_fud=wolf+saint+username'''

''''client=Connect.client()
ch=ChannelController()
dialogs=ch.getDialogs(client)
ch.storeChats(dialogs)
ch.storeChannels(dialogs,projects_ids)
#ch.storeUsers(wolf_ids,wolf)
for user in chatters:
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
#ch.printStats(ch.getDataframes(),'Waves')'''