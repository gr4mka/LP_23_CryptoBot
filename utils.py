from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Ввести пользовательские данные'], 
        ['ТОП-10 криптовалют'],
        ['subscribe','unsubscribe'],
        ['О боте']
    ])
    