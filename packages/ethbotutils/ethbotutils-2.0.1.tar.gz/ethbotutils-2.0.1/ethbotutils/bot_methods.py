import requests
import yaml


class TelegramBot:
    endpoint = "https://api.telegram.org/bot"

    def __init__(self, key):
        self.key = key
        self.debug = False
        self.offset_file = None

    def generic_bot_request(self, command, params):
        req = requests.get(TelegramBot.endpoint + self.key + "/" + command, params=params)
        return req

    def get_chat_member(self, chat_id, user_id):
        params = {"chat_id": chat_id, "user_id": user_id}
        req = self.generic_bot_request("getChatMember", params)
        print(req.json())

    def send_message(self, chat_id, text, notification=False):
        params = {"chat_id": chat_id, "text": text, "disable_notification": (not notification)}
        req = self.generic_bot_request("sendMessage", params)
        if self.debug: print(req.json())

    def send_photo(self, chat_id, photo_url):
        params = {"chat_id": chat_id, "photo": photo_url}
        req = self.generic_bot_request("sendPhoto", params)
        if self.debug: print(req.json())

    def send_gif(self, chat_id, gif_url):
        params = {"chat_id": chat_id, "animation": gif_url}
        req = self.generic_bot_request("sendAnimation", params)
        if self.debug: print(req.json())

    def send_dice(self, chat_id):
        params = {"chat_id": chat_id}
        req = self.generic_bot_request("sendDice", params)
        if self.debug: print(req.json())

    def get_my_commands(self):
        req = self.generic_bot_request("getMyCommands", {})
        print(req.json())
        return req

    def set_my_commands(self):
        commands = {"command": "help", "description": "Shows help"}
        req = self.generic_bot_request("setMyCommands", {"commands": commands})
        print(req.json())

    def get_offset(self):
        with open(self.offset_file, "r") as f:
            data = yaml.safe_load(f)
            return data["OFFSET"]

    def update_offset(self, new_offset):
        with open(self.offset_file, "r") as f1:
            data = yaml.safe_load(f1)
            data["OFFSET"] = new_offset
        with open(self.offset_file, "w") as f2:
            yaml.safe_dump(data, f2)
