from pathlib import Path

import requests

from resources.parser import read_yaml

# endpoint = "https://api.telegram.org/"
# base_path = Path(__file__).parent
# file = read_yaml(base_path / "../../config/telegram.yaml")
# key_telegram = file["TELEGRAM"]


def genericBotRequest(command, params):
    req = requests.get(endpoint + "bot" + key_telegram + "/" + command, params=params)
    return req


def getChatMember(chat_id, user_id):
    params = {"chat_id": chat_id, "user_id": user_id}
    req = genericBotRequest("getChatMember", params)
    print(req.json())


def sendMessage(chat_id, text, notification=False, debug=False):
    params = {"chat_id": chat_id, "text": text, "disable_notification": (not notification)}
    req = genericBotRequest("sendMessage", params)
    if debug: print(req.json())


def sendPhoto(chat_id, photo_url, debug=False):
    params = {"chat_id": chat_id, "photo": photo_url}
    req = genericBotRequest("sendPhoto", params)
    if debug: print(req.json())


def sendGif(chat_id, gif_url, debug=False):
    params = {"chat_id": chat_id, "animation": gif_url}
    req = genericBotRequest("sendAnimation", params)
    if debug: print(req.json())


def sendDice(chat_id, debug=False):
    params = {"chat_id": chat_id}
    req = genericBotRequest("sendDice", params)
    if debug: print(req.json())


def getMyCommands():
    req = genericBotRequest("getMyCommands", {})
    print(req.json())


def setMyCommands():
    commands = {"command": "help", "description": "Shows help"}
    req = genericBotRequest("setMyCommands", {"commands": commands})
    print(req.json())
