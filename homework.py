import os
import time
import json
import logging
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
            level=logging.INFO,
            filename='main.log',
            format='%(asctime)s; %(levelname)s; %(name)s; %(message)s',
            # filemode="w",
            )

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework['homework_name']# homework.get('homeworks')[0]['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, ' \
                  'можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    params = {
        'Authorization: OAuth <token>': 'PRAKTIKUM_TOKEN',
        'from_date': current_timestamp,
    }
    try:
        homework_statuses = requests.post(' https://praktikum.yandex.ru/api/user_api/homework_statuses/', params=params)
        # data = json.loads(homework_statuses.text)
    except BaseException as e:
        logging.exception('Ошибка получения статуса')
        raise Exception('Ошибка с запросом')
    # homework_statuses = requests.post(' https://praktikum.yandex.ru/api/user_api/homework_statuses/', params=params)
    # logging.exception('Ошибка получения статуса')
    return homework_statuses.json()


def send_message(message, bot_client):
    ...
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    # проинициализировать бота здесь
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date', current_timestamp)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
