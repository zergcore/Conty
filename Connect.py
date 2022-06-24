from telethon import TelegramClient
import telethon.sync
import configparser

class Connect:
    'Class to connect to the telegram API'
    
    def client():
    # (1) Configure your data to connect to the Telegram API. Use your own values here
        parser = configparser.ConfigParser()
        parser.read("config.txt")
        api_id=int(parser.get("config", "api_id"))
        api_hash=parser.get("config", "api_hash")
        phone=parser.get("config", "phone")
        username=parser.get("config", "username")

        # The first parameter is the .session file name (absolute paths allowed)
        client=TelegramClient(username, api_id, api_hash)

        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            myself = client.sign_in(phone, input('Enter code: '))
        #print(client.get_me())
        return client

#client=Connect.client()
#print(client.get_me())
