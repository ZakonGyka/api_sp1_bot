import json
import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

logging.basicConfig(
            level=logging.INFO,
            filename='main.log',
            format='%(asctime)s; %(levelname)s; %(name)s; %(message)s',
            filemode='w',
            )

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    try:
        homework_name = homework['homework_name']
    except:
        logging.exception('Отсутсвует имя работы')
        raise Exception('homework_name error')
    if homework['status'] == 'rejected':
        return (f'У вас проверили работу "{homework_name}"!\n\n'
                f'К сожалению в работе нашлись ошибки.')
    elif homework['status'] == 'approved':
        return (f'У вас проверили работу "{homework_name}"!\n\n'
                f'Ревьюеру всё понравилось, '
                f'можно приступать к следующему уроку.')
    else:
        return (f'У вас проверили работу "{homework_name}"!\n\n'
                f'Работа взята в ревью')


def get_homework_statuses(current_timestamp):
    current_timestamp = current_timestamp or int(time.time())
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {
        'from_date': current_timestamp,
    }
    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
            params=params, headers=headers
        )
    except BaseException as e:
        logging.exception('Ошибка получения статуса')
    return homework_statuses.json()


def send_message(message, bot_client):
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    # проинициализировать бота здесь
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(
                        new_homework.get('homeworks')[0]),
                    bot_client=Bot(token=TELEGRAM_TOKEN)
                )
            current_timestamp = new_homework.get(
                'current_date', current_timestamp
            )  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
