from glob import glob
import os
from random import choice

from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from jobs import alarm
from utils import main_keyboard


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    username = update.effective_user.username
    print("Вызван /start")
    update.message.reply_text(
        f"Здравствуй, пользователь {username}!",
        reply_markup=main_keyboard()
    )

def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {user}", reply_markup=main_keyboard())


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Вы успешно подписались')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы успешно отписались')


def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f'Уведомление через {alarm_seconds} секунд')
    except (ValueError, TypeError):
        update.message.reply_text('Введите целое число секунд после команды')
