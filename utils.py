from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Регистрация'], 
        ['Текущий курс валют', 'Ввести данные для выборки'],
        ['О боте']
    ])