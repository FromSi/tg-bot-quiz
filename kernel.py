from dotenv import load_dotenv
import sqlite
import telebot
import os


load_dotenv()


class Kernel:
    def __init__(self):
        self.sqlite = sqlite.SQLite()
        self.bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), parse_mode="MarkdownV2")

        self.BOT_MESSAGE_SEARCH_TAG = os.getenv('BOT_MESSAGE_SEARCH_TAG')
        self.BOT_POLL_TYPE = 'quiz'
        self.BOT_POLL_TITLE = os.getenv('BOT_POLL_TITLE')
        self.FILE_QUESTION_NAME = os.getenv('FILE_QUESTION_NAME')
        self.FILE_QUESTION_COUNTER_NAME = os.getenv('FILE_QUESTION_COUNTER_NAME')
        self.FILE_USER_MESSAGE_LOG_NAME = os.getenv('FILE_USER_MESSAGE_LOG_NAME')
        self.BOT_MESSAGE_SEND_START_HELP = os.getenv('BOT_MESSAGE_SEND_START_HELP')
        self.BOT_MESSAGE_SEND_START_HELP_INFO_LOG = os.getenv('BOT_MESSAGE_SEND_START_HELP_INFO_LOG')
        self.BOT_MESSAGE_SEND_START_HELP_INFO_LOG_DONE = os.getenv('BOT_MESSAGE_SEND_START_HELP_INFO_LOG_DONE')
        self.BOT_MESSAGE_SEND_START_HELP_EMOJI = os.getenv('BOT_MESSAGE_SEND_START_HELP_EMOJI')
        self.BOT_MESSAGE_SEND_REGISTER_GROUP = os.getenv('BOT_MESSAGE_SEND_REGISTER_GROUP')
        self.BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI = os.getenv('BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI')
        self.FILE_QUESTION_MARK_HANDLER = os.getenv('FILE_QUESTION_MARK_HANDLER')
        self.FILE_ANSWER_MARK_HANDLER = os.getenv('FILE_ANSWER_MARK_HANDLER')
        self.SQLITE_NAME = os.getenv('SQLITE_NAME')
        self.SQLITE_TABLE_GROUP_NAME = os.getenv('SQLITE_TABLE_GROUP_NAME')

        self.PORT = os.getenv('PORT')

        self.BOT_INTERVAL_POLLING = int(os.getenv('BOT_INTERVAL_POLLING'))
        self.BOT_TIMEOUT_POLLING = int(os.getenv('BOT_TIMEOUT_POLLING'))
