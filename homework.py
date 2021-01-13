import os
import time
import json
import logging
import requests
import telegram
from dotenv import load_dotenv
from telegram import Bot

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

# bot_client = Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    print('++')
    homework_name = homework['homework_name']# homework.get('homeworks')[0]['homework_name']
    print(homework_name)
    # homework_name = homework# homework.get('homeworks')[0]['homework_name']
    print(homework['status'])
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    elif homework['status'] == 'approved':
        verdict = 'Ревьюеру всё понравилось, ' \
                  'можно приступать к следующему уроку.'
    else:
        verdict = 'Работа взята в ревью'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {
        # 'Authorization': f'OAuth {PRAKTIKUM_TOKEN}',
        # 'from_date': 0, # Убери чтобы запустить с данного момента времени!"""
        'from_date': current_timestamp,
    }
    try:
        homework_statuses = requests.get('https://praktikum.yandex.ru/api/user_api/homework_statuses/', params=params, headers=headers)
        print(homework_statuses)
        # data = json.loads(homework_statuses.text)
        # print('***')
        # print(data)
    except BaseException as e:
        logging.exception('Ошибка получения статуса')
        raise Exception('Ошибка с запросом')
    # logging.exception('Ошибка получения статуса')
    return homework_statuses.json()


def send_message(message, bot_client):
    print('+++++')
    print(CHAT_ID)
    print(message)
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    # проинициализировать бота здесь
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            print('*-*-*--*')
            print(new_homework.get('homeworks')[0])
            if new_homework.get('homeworks'):
                print('1')
                send_message(parse_homework_status(new_homework.get('homeworks')[0]), bot_client=Bot(token=TELEGRAM_TOKEN))
            current_timestamp = new_homework.get('current_date', current_timestamp)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
