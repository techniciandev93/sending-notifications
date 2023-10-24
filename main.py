import os
import time
import traceback
import requests
import telegram
from dotenv import load_dotenv


def start_long_polling(url, headers, bot, chat_id):
    params = {}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            api_response = response.json()
            if api_response['status'] == 'timeout':
                params['timestamp'] = api_response['timestamp_to_request']
                continue

            lesson_title = api_response['new_attempts'][0]['lesson_title']
            lesson_url = api_response['new_attempts'][0]['lesson_url']
            if api_response['new_attempts'][0]['is_negative']:
                verification_message = 'К сожалению, в работе нашлись ошибки.'
            else:
                verification_message = 'Преподавателю всё понравилось, можно приступать к следующему уроку.'
            send_message = f'У вас проверили работу "{lesson_title}"\n{lesson_url}\n{verification_message}'
            bot.send_message(text=send_message, chat_id=chat_id)

            params['timestamp'] = api_response['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            traceback.print_exc()
            time.sleep(10)


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = telegram.Bot(token=telegram_token)

    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    devman_long_polling_url = 'https://dvmn.org/api/long_polling/'
    devman_headers = {'Authorization': f'Token {devman_api_token}'}
    start_long_polling(devman_long_polling_url, devman_headers, bot, telegram_chat_id)
