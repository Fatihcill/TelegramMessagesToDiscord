from queue import Queue
import requests
import threading
import ID_List
import time

class Telegram:
    _token = ""
    _call = ""
    _url = ""

    def __init__(self, token):
        self._token = token
        self._call = "https://api.telegram.org/bot%s/"
        self._url = self._call % self._token

    def post(self, method: str, **kwargs):
        r = requests.post(self._url + method, kwargs)
        return r.json()

    def get(self, method: str, **kwargs):
        r = requests.get(self._url + method, kwargs)
        return r.json()

    def getUpdates(self, timeout=50, **kwargs):
        args = ""
        for key in kwargs.keys():
            args += "&{}={}".format(key, kwargs[key])
        r = self.get(f"getUpdates?timeout={timeout}" + args, timeout=timeout + 10)
        return r

def telegramSpoof():
    print("TG Started")
    tg = Telegram(ID_List.telegram_bot_token)
    offset = 0
    while True:
        update = tg.getUpdates(timeout=50, allowed_updates=["message"], offset=offset)
        for res in update['result']:

            if "message" in res.keys():
                message = 'message'


            user_id = res[message]['from']['id']
            date = res[message]['date']

            text = res[message]['text']
            offset = res['update_id'] + 1
            data = ["TG", user_id, text, date]
            print(data)
            q.put(refactor(data))
#  {'update_id': 911861374, 'message': {'message_id': 117, 'from': {'id': 1222167633, 'is_bot': False, 'first_name': 'Fatih', 'username': 'Ziatzoraf', 'language_code': 'tr'}, 'chat': {'id': 1222167633, 'first_name': 'Fatih', 'username': 'Ziatzoraf', 'type': 'private'}, 'date': 1606213651, 'text': 'Uffff'}}

def refactor(data):  # {VK or TG} {user_id} {text} {time}
    print("AAAAAAA")
    try:
        if data[0] == "TG":
            name = ID_List.tg_table[data[1]]
    except:
        name = "Unknown"
        print(f"  Warning: user {data[1]} in {data[0]} unknown!!! ")
    avatar = ID_List.avatars[name]
    return [name, data[2], data[3], avatar]  # [{name}, {text}, {time}]


def discordSender():
    while True:
        message = q.get()
        url = ID_List.discord_webhook
        text = f"{message[1]}\n"  f"||{time.ctime(message[2])}||"
        r = requests.post(url, json={'content': text, 'username': message[0], 'avatar_url': message[3]})

        print(f"{message[0]} {message[1]} {message[2]}")


if __name__ == "__main__":
    # new thread telegramSpoof
    # new thread vkSpoof
    # create threadsafety queue
    # start discordSender
    q = Queue()

    threading.Thread(target=telegramSpoof, daemon=True).start()

    discordSender()