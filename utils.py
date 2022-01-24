from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Регистрация'], 
        ['ТОП-10 криптовалют', 'Ввести данные для выборки'],
        ['О боте']
    ])
    