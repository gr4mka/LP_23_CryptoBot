from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_predict
from utils import main_keyboard
from par import get_help_dict

def predict_start(update, context):
    update.message.reply_text(
        'Начнем! OPEN Введите стоимость криптовалюты в начале минуты(в долларах США)',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'open'


def predict_open(update, context):
    user_predict_open = update.message.text
    context.user_data['predict'] = {'open': user_predict_open}
    update.message.reply_text(
            'HIGH Введите самую высокую стоимость криптовалюты за минуту, доллар США',
            reply_markup=ReplyKeyboardRemove()
        )
    return 'high'

def predict_high(update, context):
    user_predict_high = update.message.text
    context.user_data['predict'] = {'high': user_predict_high}
    update.message.reply_text(
            'LOW Введите самую низкую стоимость криптовалюты за минуту, доллар США',
            reply_markup=ReplyKeyboardRemove()
        )
    return 'low'

def predict_low(update, context):
    user_predict_low = update.message.text
    context.user_data['predict'] = {'low': user_predict_low}
    update.message.reply_text('VOLUME Введите количество единиц криптовалюты, проданных или купленных в течение минуты',reply_markup=ReplyKeyboardRemove())
    return 'volume'

def predict_volume(update, context):
    user_predict_volume = update.message.text
    context.user_data['predict'] = {'volume': user_predict_volume}
    update.message.reply_text('VWAP редневзвешенная стоимость криптовалюты за минуту, доллар США',reply_markup=ReplyKeyboardRemove())
    return 'vwap'

def predict_vwap(update, context):
    user_predict_vwap = update.message.text
    context.user_data['predict'] = {'vwap': user_predict_vwap}
    reply_keyboard = [['Предсказать']]
    update.message.reply_text('Предсказать!', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 'result'


def predict_result(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_predict(db, user['user_id'], context.user_data['predict'])
    predict_text = format_predict(context.user_data['predict'])
    update.message.reply_text(predict_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_predict(predict):
    predict_text = f"""
                <b>open</b>: {predict['open']}
                <b>high</b>: {predict['high']}
                <b>low</b>: {predict['low']}
                <b>volume</b>: {predict['volume']}
                <b>vwap</b>: {predict['vwap']}
"""
    return predict_text

def predict_dontknow(update, context):
    update.message.reply_text('Введены некорректные данные')