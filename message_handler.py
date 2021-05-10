import threading
from time import sleep
import kernel


def bot_polling():
    while True:
        app = kernel.Kernel()

        try:
            bot_actions(app)
            app.bot.polling(none_stop=True, interval=app.BOT_INTERVAL_POLLING, timeout=app.BOT_TIMEOUT_POLLING)
        except Exception as ex:
            app.bot.stop_polling()
            sleep(app.BOT_TIMEOUT_POLLING)
        else:
            app.bot.stop_polling()
            break


def bot_actions(app):
    @app.bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_START_HELP)
        app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_START_HELP_EMOJI)

    @app.bot.message_handler(content_types=['new_chat_members'])
    def register_group(message):
        is_add_group = app.sqlite.add_group(message.chat.id)

        if is_add_group:
            app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_REGISTER_GROUP)
            app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI)


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
