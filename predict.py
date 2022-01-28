from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_predict
from utils import main_keyboard
from par import get_help_dict
import pandas as pd

import joblib

#загрузка модели
model = joblib.load("C:/projects/newbot/saved_models/Bitcoin_model")



def predict_start(update, context):
    update.message.reply_text(
        'Начнем! \n<b>OPEN</b> \nВведите стоимость криптовалюты в начале минуты(в долларах США)', parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )
    return 'open'


def predict_open(update, context):
    user_predict_open = update.message.text
    #if type(user_predict_open) != float:
    #    update.message.reply_text('Пожалуйста, введите число')
    #    return 'open'
    #else:
    context.user_data['predict'] = {'Open': user_predict_open}
    update.message.reply_text(
            '<b>HIGH</b> \nВведите самую высокую стоимость криптовалюты за минуту, доллар США', parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
    return 'high'

def predict_high(update, context):
    user_predict_high = update.message.text
    context.user_data['predict'].update({'High': user_predict_high})
    update.message.reply_text(
            '<b>LOW</b> \nВведите самую низкую стоимость криптовалюты за минуту, доллар США', parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
    return 'low'

def predict_low(update, context):
    user_predict_low = update.message.text
    context.user_data['predict'].update({'Low': user_predict_low})
    update.message.reply_text('<b>Close</b> \nВведите цену в конце минуты', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return 'close'

def predict_close(update, context):
    user_predict_close = update.message.text
    context.user_data['predict'].update({'Close': user_predict_close})
    update.message.reply_text('<b>VOLUME</b> \nВведите количество единиц криптовалюты, проданных или купленных в течение минуты', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return 'volume'    

def predict_volume(update, context):
    user_predict_volume = update.message.text
    context.user_data['predict'].update({'Volume': user_predict_volume})
    update.message.reply_text('<b>VWAP</b> \nВведите средневзвешенную стоимость криптовалюты за минуту, доллар США', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return 'vwap'

def predict_vwap(update, context):
    user_predict_vwap = update.message.text
    context.user_data['predict'].update({'VWAP': user_predict_vwap})
    reply_keyboard = [['Предсказать!']]
    update.message.reply_text('Предсказать?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 'result'


def predict_result(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    predict_text = format_predict(context.user_data)
    save_predict(db, user['user_id'], context.user_data['predict'])
    update.message.reply_text(predict_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_predict(predict):
#    predict_text = str(predict['predict'])
#    x = pd.DataFrame({'Open':[1], 'High':[2], 'Low':[3], 'Close':[6], 'Volume':[4], 'VWAP':[5]})
#    
    n_predict = {}
    for lable, val in (predict['predict']).items():
        n_predict[lable] = [val]
    #    predict_text = str(n_predict)
    x = pd.DataFrame(n_predict)
    predict_text = str(model.predict(x))
    return predict_text

def predict_dontknow(update, context):
    update.message.reply_text('Введены некорректные данные')