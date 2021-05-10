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


def user_message_log(app, message):
    with open(app.FILE_USER_MESSAGE_LOG_NAME, 'a') as file:
        file.write('-------------------\n')
        file.write("{0}: {1}\n".format('message_id', message.message_id))
        file.write("{0}: {1}\n".format('user_id', message.from_user.id))
        file.write("{0}: {1}\n".format('first_name', message.from_user.first_name))
        file.write("{0}: {1}\n".format('last_name', message.from_user.last_name))
        file.write("{0}: {1}\n".format('username', message.from_user.username))
        file.write("{0}: {1}\n".format('date', message.date))
        file.write('-------------------\n')
        file.write(message.text)
        file.write('\n-------------------\n')
        file.write('\n\n\n')


def bot_actions(app):
    @app.bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_START_HELP)
        app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_START_HELP_INFO_LOG)
        app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_START_HELP_EMOJI)

    @app.bot.message_handler(content_types=['new_chat_members'])
    def register_group(message):
        is_add_group = app.sqlite.add_group(message.chat.id)

        if is_add_group:
            app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_REGISTER_GROUP)
            app.bot.send_message(message.chat.id, app.BOT_MESSAGE_SEND_REGISTER_GROUP_EMOJI)

    @app.bot.message_handler(func=lambda message: message.chat.type == 'private')
    def message_log(message):
        user_message_log(app=app, message=message)
        app.bot.reply_to(message, app.BOT_MESSAGE_SEND_START_HELP_INFO_LOG_DONE)


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
