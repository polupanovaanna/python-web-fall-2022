# python-web-fall-2022
Python web course homework project

# О приложении
Веб-приложение, имитирующее систему для поиска и бронирования отелей 

# Запуск

Можно запустить из консоли с помощью команды `uvicorn app.main:app --reload`

Кроме того, с ветки hw2 закоммичена папка с настройками проекта для vscode, поэтому внутри vscode проект можно собрать автоматически

Запустить тесты можно командой `python3.10 -m unittest discover -s app/ -p "tests*"`

# Существующая бизнес-логика

Сейчас все работает на игрушечной базе данных внутри приложения

- Работа с бронированиями
    - Совершение нового бронирования. Объект бронирования добавляется в базу данных
    - Получение информации о бронировании по его id
    - Получение инфомации о всех существующих бронированиях пользователя

# GRPC

Появилась отдельная компонента с той же самой логикой, что и в основном приложении, но с grpc

Поднять сервер: `python3.10 grpc_booking_service/booking_process_server.py`

Поднять клиент: `python3.10 grpc_booking_service/booking_process_client.py`

Запуск тестов из папки grpc_booking_service: `python3.10 -m unittest discover -p "tests*"`
