import requests
import json
import urllib
from settings import *


class Bot:
    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot{}/".format(token)

    @staticmethod
    def context(message):
        text = message["message"]["text"]
        chat = message["message"]["chat"]["id"]
        return text, chat

    @staticmethod
    def get_url(url: str) -> str:
        response = requests.get(url, timeout=30)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.url + "getUpdates?timeout=500"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    @staticmethod
    def get_last_update_id(updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = self.url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def echo(self, updates):
        for update in updates["result"]:
            text, chat = self.context(update)
            self.send_message(text, chat)


if __name__ == '__main__':
    print(TRY_RUN_MODULE)
