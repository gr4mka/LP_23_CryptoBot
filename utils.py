from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Ввести пользовательские данные'],
        ['Предсказание'],
        ['ТОП-10 криптовалют'],
        ['subscribe','unsubscribe'],
        ['О боте']
    ])
    