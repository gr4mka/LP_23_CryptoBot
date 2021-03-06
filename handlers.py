from glob import glob
import os
from telegram import ParseMode
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from db import db, get_or_create_user, subscribe_user, unsubscribe_user
#from jobs import alarm
from utils import main_keyboard
import settings
import json
import pprint
import dpath.util as dp   #  pip install dpath

def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print("Вызван /start")
    update.message.reply_text(
        f"Здравствуй, пользователь {user['username']}!",
        reply_markup=main_keyboard()
    )

def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text}", reply_markup=main_keyboard())


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Вы успешно подписались')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы успешно отписались')

def about(update, context):
    text = 'Бот разработан в рамках обучающего курса Learn Python, 23й набор (2022)'
    update.message.reply_text(f"{text}", reply_markup=main_keyboard())

def current_info(update, context):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start': '1',
    'limit':'10',
    'convert':'USD'
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': settings.COINMARKETCAP
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        coins = json.loads(response.text)['data']
        for n in coins:
            info = f"""<b>Название</b>: {n['name']}
<b>Символ</b>: {n['symbol']}
<b>Текущий курс ($)</b>: {n['quote']['USD']['price']}
<b>Процентное изменение за час:</b>: {n['quote']['USD']['percent_change_1h']}
"""
            update.message.reply_text(info, parse_mode=ParseMode.HTML)
        pprint.pprint(coins)
#        values = dp.values(coins, "/name/**/symbol")
#        print(values)



    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
"""
def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f'Уведомление через {alarm_seconds} секунд')
    except (ValueError, TypeError):
        update.message.reply_text('Введите целое число секунд после команды')
"""        