import logging
import os
import time
import traceback
import requests
import telegram
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start_long_polling(url, headers, bot, chat_id):
    params = {}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            proven_work = response.json()
            if proven_work['status'] == 'timeout':
                params['timestamp'] = proven_work['timestamp_to_request']
                continue

            lesson_title = proven_work['new_attempts'][0]['lesson_title']
            lesson_url = proven_work['new_attempts'][0]['lesson_url']
            if proven_work['new_attempts'][0]['is_negative']:
                verification_message = 'К сожалению, в работе нашлись ошибки.'
            else:
                verification_message = 'Преподавателю всё понравилось, можно приступать к следующему уроку.'
            send_message = f'У вас проверили работу "{lesson_title}"\n{lesson_url}\n{verification_message}'
            bot.send_message(text=send_message, chat_id=chat_id)

            params['timestamp'] = proven_work['last_attempt_timestamp']
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

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))

    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    devman_long_polling_url = 'https://dvmn.org/api/long_polling/'
    devman_headers = {'Authorization': f'Token {devman_api_token}'}

    try:
        logger.info('Бот запущен')
        start_long_polling(devman_long_polling_url, devman_headers, bot, telegram_chat_id)
    except Exception as error:
        bot.send_message(text='Бот упал с ошибкой:', chat_id=telegram_chat_id)
        logger.error(error)
