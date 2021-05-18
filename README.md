# tg-bot-quiz

Код телеграм бота, который способен доставлять в существующих им чатах, вопросы (quiz). Ничто не мешает запустить своего бота со своими вопросами (будет инструкция).

## Возможности
* Приветствовать как в личных сообщениях, так и при заходе в чат
* Записывает текст с личных сообщений (журнал предложений)
* Выставление в вопросе хештега (метка для поиска старых вопросов)
* Счетчик отправленных вопросов (чтобы не повторялся старый)
* Если вопросы кончатся, будет выбираться рандомный (когда появится новый вопрос, он будет следующим)
* Вопрос может содержать [markdown](https://core.telegram.org/bots/api#markdownv2-style) и отступы (чтобы в несколько строк и со стилями)

__Бонус:__ всё необходимое в `.env.example`

Еще пишу... В работе...

## Установка
1) Склонировать репозиторий -> `git clone https://github.com/FromSi/tg-bot-quiz.git`
2) Сделать -> `cp .env.example .env`
3) Запуск бота -> `make run`
4) Настроить в CRON команду для создания вопроса -> `make create_quiz`

## Запуск бота
Бота нужно запускать через `Makefile`.

Запуск `message_handler.py` – `make run`

Остановка `message_handler.py` – `make stop`

Запуск `create_quiz.py` – `make create_quiz` (перед этим нужно запустить `message_handler.py`)

## Две входные точки
Существуют две входные точки `message_handler.py` и `create_quiz.py`.

### message_handler.py
Точка запускается с Docker'ом. Он обрабатывает регистрацию в приватных диалогах пользователей и чатов.

### create_quiz.py
Точку необходимо запускать в ручную, через скрипт или CRON. Это event для создания QUIZ в чатах.

## Ведение вопросов
Все вопросы лежат в файле `questions.txt`.

Все вопросы в \[q\] могут быть записаны с отступами и обязательно следовать [markdown](https://core.telegram.org/bots/api#markdownv2-style).

Ответы в \[a\] должны быть в одну линию и не превышать 300 символов. [См документацию](https://core.telegram.org/bots/api#sendpoll)

## Описание создаваемых файлов (в игноре git)
* `question_counter.txt` – счетчик заданных вопросов
* `sqlite.db` – база данных
* `user_message_log.txt` – записывание сообщений из приватных диалогов с пользователем
* `.env` – настройка бота

## Описание .env
* BOT_TOKEN – токен бота, полученный от [BotFather](https://t.me/BotFather)
* BOT_INTERVAL_POLLING – polling бота с его interval
* BOT_TIMEOUT_POLLING – polling бота с его timeout
* BOT_MESSAGE_SEND_START_HELP – сообщение приветствия в диалоге пользователя
* BOT_MESSAGE_SEND_START_HELP_INFO_LOG – сообщение о том, что диалоги с пользователем будут логироваться
* BOT_MESSAGE_SEND_START_HELP_INFO_LOG_DONE – успешное сообщение залогированного сообщения пользователя в диалогах
* BOT_MESSAGE_SEND_START_HELP_EMOJI – emoji приветствия в диалоге пользователя
* BOT_MESSAGE_SEND_REGISTER_GROUP – сообщение при добавлении бота в чат
* BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI – emoji при добавлении бота в чат
* BOT_MESSAGE_SEARCH_TAG – хештег для поиска по чату
* BOT_POLL_TITLE – заголовок в блоке вопроса
* FILE_QUESTION_NAME – название файла для вопросов
* FILE_QUESTION_MARK_HANDLER – метка вопросов
* FILE_ANSWER_MARK_HANDLER – метка ответов
* FILE_QUESTION_COUNTER_NAME – название файла для счетчика вопросов
* FILE_USER_MESSAGE_LOG_NAME – название файла для записи сообщений пользователей с диалогов
* SQLITE_FILE_NAME – название файла базы данных
* SQLITE_TABLE_GROUP_NAME – название таблицы зарегистрированных чатов
