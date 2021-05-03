import sqlite
import telebot
import threading
import os
from time import sleep
from dotenv import load_dotenv


load_dotenv()


SQLITE = sqlite.SQLite()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_INTERVAL = int(os.getenv('BOT_INTERVAL'))
BOT_TIMEOUT = int(os.getenv('BOT_TIMEOUT'))

BOT_MESSAGE_SEND_START_HELP = os.getenv('BOT_MESSAGE_SEND_START_HELP')
BOT_MESSAGE_SEND_START_HELP_EMOJI = os.getenv('BOT_MESSAGE_SEND_START_HELP_EMOJI')
BOT_MESSAGE_SEND_REGISTER_GROUP = os.getenv('BOT_MESSAGE_SEND_REGISTER_GROUP')
BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI = os.getenv('BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI')


def bot_polling():
    while True:
        bot = telebot.TeleBot(BOT_TOKEN)

        try:
            bot_actions(bot)
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex:
            print("Bot polling failed, restarting in {0}sec. Error:\n{1}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else:
            bot.stop_polling()
            print("Bot polling loop finished")
            break


def bot_actions(bot):
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, BOT_MESSAGE_SEND_START_HELP)
        bot.send_message(message.chat.id, BOT_MESSAGE_SEND_START_HELP_EMOJI)

    @bot.message_handler(content_types=['new_chat_members'])
    def register_group(message):
        is_add_group = SQLITE.add_group(message.chat.id)

        if is_add_group:
            bot.send_message(message.chat.id, BOT_MESSAGE_SEND_REGISTER_GROUP)
            bot.send_message(message.chat.id, BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI)


polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


if __name__ == "__main__":
    """https://gist.github.com/David-Lor/37e0ae02cd7fb1cd01085b2de553dde4"""
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break
