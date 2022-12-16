# Проектная работа 7 спринта

У меня создавались миграции в https://github.com/mburdonos/Auth_sprint_2/blob/master/flask_app/entrypoint.sh
Почему так нельзя было?

Сервис аутентификации: https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app

стркутура: точки запроса https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app/api/v1 базовые настройки https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app/core класс и методы по взаимодействиб с бд(postgresql) https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app/db модели БД https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app/models тесты https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app/tests полезные функции, вынесенные отдельно https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app/utils

Описание сервиса: Сервис аутентификации, позволяющий создавать новых пользователей, авторизоваться и в зависимости от прав пользователя, получать определенные данные

Аутентификация происходит по login или email (в зависимости от способа необходимо передавать параметр)
так же реализована регистрация и авторизация через yandex:

http://127.0.0.1:5000/api/v1/register/yandex и http://127.0.0.1:5000/api/v1/login/yandex

для защиты от DDos атак реализована защита в nginx посредством Leaky bucket

к точкам http://127.0.0.1:5000/api/v1/register и http://127.0.0.1:5000/api/v1/login можно обратиться всем пользователям

к остальным только авторизованым пользователям, при этом к ряду точек добавлено разграничение прав, например:

создать роль http://127.0.0.1:5000/api/v1/roles/create сможет только пользователь с правами "admin" или же получить список всех пользователей http://127.0.0.1:5000/api/v1/users смогут получить "admin" и "staff"

Подробно можно ознакомиться с документацией https://github.com/mburdonos/Auth_sprint_2/blob/master/flask_app/openapi.json

Запуск сервиса: через докер:

создать .env файл с настройками из https://github.com/mburdonos/Auth_sprint_2/blob/master/flask_app/core/config.py и запусть docker-compose up -d в https://github.com/mburdonos/Auth_sprint_2/tree/master/

без докера: создать .env файл с настройками из https://github.com/mburdonos/Auth_sprint_2/blob/master/flask_app/core/config.py python main.py в https://github.com/mburdonos/Auth_sprint_2/tree/master/flask_app
