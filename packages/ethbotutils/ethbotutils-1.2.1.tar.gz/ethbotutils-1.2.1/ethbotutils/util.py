from pathlib import Path

import requests

from resources.parser import read_yaml

# base_path = Path(__file__).parent
# file = read_yaml(base_path / "../../../config/keys.yaml")
# key_cryptocompare = file["CRYPTOCOMPARE"]
# key_defipulse = file["DEFIPULSE"]
# key_etherscan = file["ETHERSCAN"]


def convertCurrency(key_cryptocompare, fromSym, toSym):
    params = {"fsym": fromSym, "tsyms": toSym, "extraParams": "CryptoBot"}
    req = requests.get(
        "https://min-api.cryptocompare.com/data/price?" + key_cryptocompare,
        params=params)
    if req.ok: return req.json()[toSym]


def getFromEthGasStation(category):
    r = requests.get(
        "https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key"
        "=" + key_defipulse)
    if r.ok:
        json = r.json()
        selectedCategory = json[category]
        return selectedCategory / 10


def gweiToEth(gweiAmount):
    gas = 21000 * gweiAmount
    return gas / 1000000000


def digitFormat(toConvert, digits=2):
    my_format = '{:.' + str(digits) + 'f}'
    return my_format.format(toConvert)


def getWalletAmount(address):
    r = requests.get("https://api.etherscan.io/api?module=account&action=balance&address="
                     + str(address) + "&tag=latest&apikey="
                     + key_etherscan)
    wei = float(r.json()["result"])
    return wei / 1000000000000000000
