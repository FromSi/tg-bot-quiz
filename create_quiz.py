import telebot
import sqlite
import os
from dotenv import load_dotenv


load_dotenv()


SQLITE = sqlite.SQLite()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT = telebot.TeleBot(BOT_TOKEN)
GROUPS = SQLITE.get_groups()
BOT_POLL_TYPE = 'quiz'
BOT_POLL_TITLE = os.getenv('BOT_POLL_TITLE')


class QuestionQuiz:
    def __init__(self):
        self.question = ''
        self.answers = []


def get_question_quiz_by_file(question_number, file):
    question_quiz = QuestionQuiz()

    for fileline in file:
        if fileline[0:3] == '[q]':
            if question_number == 0:
                question_quiz.question += fileline[3:]

                break
            else:
                question_number -= 1

    for fileline in file:
        if fileline[0:3] == '[a]':
            question_quiz.answers.append(fileline[3:])

            break

        question_quiz.question += fileline

    for fileline in file:
        if fileline[0:3] == '[q]':
            break
        else:
            question_quiz.answers.append(fileline[3:])

    return question_quiz


def get_correct_question_number_by_file(question_number, file):
    amount_questions = 0

    for fileline in file:
        if fileline[0:3] == '[q]':
            amount_questions += 1

    return question_number % amount_questions


def get_question(question_number=0):
    with open('questions.txt', 'r') as file:
        question_number = get_correct_question_number_by_file(question_number, file)

    with open('questions.txt', 'r') as file:
        question_quiz = get_question_quiz_by_file(
            question_number,
            file,
        )

        return question_quiz


def send_poll(gid, options, correct_option_id):
    BOT.send_poll(
        chat_id=gid,
        question=BOT_POLL_TITLE,
        options=options,
        is_anonymous=False,
        type=BOT_POLL_TYPE,
        correct_option_id=correct_option_id,
    )


def create_quiz(question, options):
    for group in GROUPS:
        gid = group[0]

        BOT.send_message(gid, question)

        send_poll(
            gid=gid,
            options=options,
            correct_option_id=0
        )


def get_question_number():
    return 0


def main():
    question_quiz = get_question(get_question_number())
    create_quiz(
        question=question_quiz.question,
        options=question_quiz.answers
    )


main()

# Считывание ответов (рандомизация)
# настроить get_question_number()
# Настроить README.md
# Донастроить бота по созданию quiz