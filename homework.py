import logging
import os
import time

import requests

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
    homework_name = homework.get('homework_name')
    if homework_name is None:
        logging.exception('Отсутсвует название домашней работы')
        homework_name = 'Отсутсвует название домашней работы'

    status = homework.get('status')

    status_dict = {'rejected': f'У вас проверили работу "{homework_name}"!\n\n'
                               'К сожалению в работе нашлись ошибки.',
                   'approved': f'У вас проверили работу "{homework_name}"!\n\n'
                               'Ревьюеру всё понравилось, '
                               'можно приступать к следующему уроку.',
                   'reviewing': f'Работа "{homework_name}" взята на ревью'}

    if status in status_dict:
        return status_dict[status]
    logging.error('Получен неизвестный статус')
    return 'Получен неизвестный статус'


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
    except ConnectionError:
        logging.exception('Ошибка получения статуса')
        return {}
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
