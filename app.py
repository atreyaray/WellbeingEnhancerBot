from dotenv import load_dotenv
import settings
import os
import requests
import json
import pymongo
import telegram.ext
import configparser as cfg




def main() :

    class telegram_chatbot():
        def __init__(self, config):
            self.token = self.read_token_from_config_file(config)
            self.base = "https://api.telegram.org/bot{}/".format(self.token)

        def get_updates(self, offset=None):
            url = self.base + "getUpdates?timeout=100"
            if offset:
                url = url + "&offset={}".format(offset + 1)
            r = requests.get(url)
            return json.loads(r.content)

        def send_message(self, msg, chat_id):
            url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
            if msg is not None:
                requests.get(url)

        def read_token_from_config_file(self, config):
            parser = cfg.ConfigParser()
            parser.read(config)
            return parser.get('creds', 'token')

    # db_uri = f'mongodb+srv://teamstemboys:{settings.DATABASE_PASSWORD}@cluster0.aakcb.mongodb.net/<dbname>?retryWrites=true&w=majority'
    # client = pymongo.MongoClient(db_uri)
    # set up database
    # db = client.test
    print('hello')
    bot = telegram_chatbot("config.cfg")
    update_id = None
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    print(updates)
    print('ends')


    # bot = Bot(settings.TOKEN)

    # Adding a new user
    # user = {"name" : "sergey" , "last_name": "zakuraev"}
    # users = db.users
    # users.insert_one(user)
    # pass

if __name__ == "__main__":
    main()
