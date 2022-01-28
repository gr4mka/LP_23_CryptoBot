from glob import glob
import os
from telegram import ParseMode
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from utils import main_keyboard
import settings
import json
import pprint
import dpath.util as dp   #  pip install dpath
def get_help_dict():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start': '1',
    'limit':'30',
    'convert':'USD'
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': settings.COINMARKETCAP
    }

    session = Session()
    session.headers.update(headers)


    response = session.get(url, params=parameters)
    coins = json.loads(response.text)['data']
    ab = []
    for n in coins:
            ab.append(n['name']+' '+n['symbol'])
#   ab = "".join(ab)
    print(ab)
    return ab
