from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_anketa
from utils import main_keyboard
from par import get_help_dict

def anketa_start(update, context):
    update.message.reply_text(
        'Здравствуйте! Как к Вам обращаться? (Введите имя, без цифр и символов)',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'


def anketa_name(update, context):
    user_name = update.message.text
    if str.isalpha(user_name) is False:
        update.message.reply_text('Пожалуйста, введите Ваше имя(только текст)')
        return 'name'
    else:
        context.user_data['anketa'] = {'name': user_name}
        reply_keyboard = [['Bitcoin BTC', 'Etherium ETH', 'BNB BNB'],
                         ['Tether USDT', 'Lightcoin LTC', 'Dogecoin DOGE'],
                         ['help']]
        update.message.reply_text(
            'Выберите интресующую Вас криптовалюту, либо ипользуйте /help для вывода всех доступных криптовалют',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'choice'

def crypto_help(update, context):
        reply_keyboard = [['Bitcoin BTC', 'Etherium ETH', 'BNB BNB'],
                         ['Tether USDT', 'Lightcoin LTC', 'Dogecoin DOGE'],
                         ['help']]
        update.message.reply_text(
            get_help_dict(),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

def anketa_time(update, context):
        reply_keyboard = [['5 минут', '10 минут', '15 минут'],
                         ['30 миут', '1 час', '1 день'],
                         ['help']]
        update.message.reply_text(
            get_help_dict(),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        update.message.reply_text('Напишите комментарий, или выберите /skip, чтобы пропустить')
        return 'time'

def anketa_choice(update, context):
    context.user_data['anketa']['choice'] = str(update.message.text)
    update.message.reply_text('Напишите комментарий, или выберите /skip, чтобы пропустить')
    return 'comment'

def anketa_comment(update, context):
    context.user_data['anketa']['comment'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f"""<b>Имя Пользователя</b>: {anketa['name']}
<b>Интересующая валюта</b>: {anketa['choice']}
"""
    if 'comment' in anketa:
        user_text += f"\n<b>Комментарий</b>: {anketa['comment']}"
    return user_text


def anketa_dontknow(update, context):
    update.message.reply_text('Введены некорректные данные')
