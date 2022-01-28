from datetime import time
import logging
import pytz

from telegram.bot import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext import messagequeue as mq
#from telegram.ext.jobqueue import Days
from telegram.utils.request import Request

from anketa import (anketa_start, anketa_name, crypto_help, anketa_choice, anketa_skip, anketa_comment,
                    anketa_dontknow)

from handlers import (greet_user, current_info,
                      talk_to_me, subscribe, unsubscribe, about)#, set_alarm)  

from predict import predict_start, predict_open, predict_dontknow, predict_high, predict_low, predict_volume, predict_vwap, predict_result

from jobs import send_updates
from par import get_help_dict
import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)

#PROXY = {'proxy_url': settings.PROXY_URL,
#         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

"""
class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()
    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)
"""

def main():
#    request = Request(
#        con_pool_size=8,
#        proxy_url=PROXY['proxy_url'],
#        urllib3_proxy_kwargs=PROXY['urllib3_proxy_kwargs']
#    )
#    bot = MQBot(settings.API_KEY, request=request)
#    bot = Updater(settings.API_KEY, use_context=True)
#    cbot = Updater(bot=bot, use_context=True)
    cbot = Updater(settings.API_KEY, use_context=True)

#    jq = mybot.job_queue
#    target_time = time(12, 0, tzinfo=pytz.timezone('Europe/Moscow'))
#    target_days = (Days.MON, Days.WED, Days.FRI)
#    jq.run_daily(send_updates, target_time)#, target_days)

    dp = cbot.dispatcher

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Ввести пользовательские данные)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "choice": [
                CommandHandler('help', crypto_help),
                MessageHandler(Filters.regex('^(help)$'), crypto_help),
                MessageHandler(Filters.text, anketa_choice),
                MessageHandler(Filters.regex('^(Bitcoin BTC|Etherium ETH|BNB BNB|Tether USDT|Lightcoin LTC|Dogecoin DOGE)$'), anketa_choice),
                ],
            "comment": [
                CommandHandler('skip', anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ]
        },
        fallbacks=[
            MessageHandler(
                Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location,
                anketa_dontknow
            )
        ]
    )

    predict = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Предсказание)$'), predict_start)
        ],
        states={
            "open": [MessageHandler(Filters.text, predict_open)],
            "high": [MessageHandler(Filters.text, predict_high)],
            "low": [MessageHandler(Filters.text, predict_low)],
            "volume": [MessageHandler(Filters.text, predict_volume)],
            "vwap": [MessageHandler(Filters.text, predict_vwap)],
            "result": [MessageHandler(Filters.text, predict_result)]

        },
        fallbacks=[
            MessageHandler(
                Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location,
                predict_dontknow
            )
        ]
    )
    
    dp.add_handler(anketa)
    dp.add_handler(predict)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('registration', anketa_start))
    dp.add_handler(CommandHandler('predict', predict_start))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('top10', current_info))
    dp.add_handler(MessageHandler(Filters.regex('^(ТОП-10 криптовалют)$'), current_info))
    dp.add_handler(MessageHandler(Filters.regex('^(Ввести пользовательские данные)$'), anketa_start))
    dp.add_handler(MessageHandler(Filters.regex('^(Предсказание)$'), predict_start))
    dp.add_handler(MessageHandler(Filters.regex('^(О боте)$'), about))
    dp.add_handler(MessageHandler(Filters.regex('^(subscribe)$'), subscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(unsubscribe)$'), unsubscribe))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    cbot.start_polling()
    cbot.idle()


if __name__ == "__main__":
    main()
    