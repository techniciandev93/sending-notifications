# Отправляем уведомления о проверке работ в телеграмм

Этот скрипт предназначен для отправки уведомлений проверенных работ на курсах [dvmn.org](https://dvmn.org/)

## Как установить

Python 3.8 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Создайте файл `.env` в корневой директории проекта и добавьте переменные окружения:

```
DEVMAN_API_TOKEN= devman токен
TELEGRAM_TOKEN= токен телеграмм бота
TELEGRAM_CHAT_ID= ID в телеграмме
TELEGRAM_NOTIFICATION_TOKEN=токен для 2 бота уведомлений
```
## Как запустить
Запустите скрипт
```
python main.py
```

## Запустить в Docker
Собрать проект
```
docker build -t techniciandev93/sending-notifications:v1 .
```
Запустить проект
```
docker run --env-file .env -d techniciandev93/sending-notifications:v1
```
Для установки докера воспользуйтесь [документацией.](https://docs.docker.com/engine/install/)
## Примечания

- Для работы скрипта необходимо иметь 2 API-токена Telegram (1 бот для отправки уведомлений о проверенных работах, 2 бот для отправки уведомлений о работе 1 бота). Вы можете получить их, создав ботов через [BotFather](https://core.telegram.org/bots#botfather).
- Для корректной работы скрипта, убедитесь, что у вас есть `chat_id`, который представляет уникальный идентификатор чата в Telegram. Можно узнать сво ID  у бота [userinfobot](https://t.me/userinfobot).
- Для работы с API Devman необходимо ознакомиться с [документацией](https://dvmn.org/api/docs/).

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).