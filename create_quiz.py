import telebot
import sqlite
import os
from dotenv import load_dotenv


# load_dotenv()
#
#
# SQLITE = sqlite.SQLite()
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# BOT = telebot.TeleBot(BOT_TOKEN)
# GROUPS = SQLITE.get_groups()
# BOT_POLL_TYPE = 'quiz'
# BOT_POLL_TITLE = os.getenv('BOT_POLL_TITLE')
#
#
# def send_poll(gid, options, correct_option_id):
#     BOT.send_poll(
#         chat_id=gid,
#         question=BOT_POLL_TITLE,
#         options=options,
#         is_anonymous=False,
#         type=BOT_POLL_TYPE,
#         correct_option_id=correct_option_id,
#     )
#
#
# def create_quiz(question, options):
#     for group in GROUPS:
#         gid = group[0]
#
#         BOT.send_message(gid, question)
#
#         send_poll(
#             gid=gid,
#             options=options,
#             correct_option_id=0
#         )
#
#
# create_quiz(
#     question='Title',
#     options=['Да', 'Нет']
# )


def get_question_by_file(question_number, file):
    for fileline in file:
        if fileline[0:3] == '[q]':
            if question_number == 0:
                return fileline
            else:
                question_number -= 1

    return None


def get_correct_question_number_by_file(question_number, file):
    amount_questions = 0

    for fileline in file:
        if fileline[0:3] == '[q]':
            amount_questions += 1
    print(amount_questions)
    return question_number % amount_questions


def get_question(question_number=0):
    with open('questions.txt') as file:
        print(get_correct_question_number_by_file(question_number, file))
        question = get_question_by_file(
            get_correct_question_number_by_file(question_number, file),
            file,
        )
        print(question)


get_question(0)
get_question(1)
get_question(2)
get_question(3)
get_question(4)


# Правильное вычисление get_correct_question_number_by_file
# Правильно считывать вопрос (с отступами)
# Считывание ответов (рандомизация)
# Настроить README.md
# Донастроить бота по созданию quiz