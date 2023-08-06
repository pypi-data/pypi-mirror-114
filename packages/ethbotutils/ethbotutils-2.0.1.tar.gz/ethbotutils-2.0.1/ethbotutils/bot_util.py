import requests
import yaml


def convert_currency(key_cryptocompare, fromSym, toSym):
    params = {"fsym": fromSym, "tsyms": toSym, "extraParams": "CryptoBot"}
    req = requests.get(
        "https://min-api.cryptocompare.com/data/price?" + key_cryptocompare,
        params=params)
    if req.ok: return req.json()[toSym]


def get_from_ethgasstation(key_defipulse, category):
    r = requests.get(
        "https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key"
        "=" + key_defipulse)
    if r.ok:
        json = r.json()
        selectedCategory = json[category]
        return selectedCategory / 10


def gwei_to_eth(gweiAmount):
    gas = 21000 * gweiAmount
    return gas / 1000000000


def digit_format(toConvert, digits=2):
    my_format = '{:.' + str(digits) + 'f}'
    return my_format.format(toConvert)


def get_wallet_amount(key_etherscan, address):
    r = requests.get("https://api.etherscan.io/api?module=account&action=balance&address="
                     + str(address) + "&tag=latest&apikey="
                     + key_etherscan)
    wei = float(r.json()["result"])
    return wei / 1000000000000000000


def load_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("YAML file not found")
    except yaml.YAMLError as exc:
        print("Invalid YAML file")
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
