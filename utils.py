#from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
#from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
#from clarifai_grpc.grpc.api.status import status_code_pb2
from random import randint
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Прислать котика', KeyboardButton('Мои координаты', request_location=True), 'Заполнить анкету']
    ])