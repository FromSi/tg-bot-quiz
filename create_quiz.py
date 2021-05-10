import kernel
import random


class QuestionQuiz:
    """Класс для вопроса и его ответов"""
    def __init__(self):
        self.question = ''
        self.options = []


def create_telegram_quiz(app, question, options, correct_option_id):
    """Создание ботом телеграма переданного вопроса в зарегистрированные группы"""
    groups = app.sqlite.get_groups()

    for group in groups:
        gid = group[0]

        app.bot.send_message(gid, question)

        app.bot.send_poll(
            chat_id=gid,
            question=app.BOT_POLL_TITLE,
            options=options,
            is_anonymous=False,
            type=app.BOT_POLL_TYPE,
            correct_option_id=correct_option_id,
        )


def get_question_quiz(app, question_number=0):
    """Получение QuestionQuiz объекта по средством обработки файла"""
    question_quiz = QuestionQuiz()

    with open(app.FILE_QUESTION_NAME, 'r') as file:
        for fileline in file:
            """Находка нужного вопроса. Ставим курсор."""
            if fileline[0:3] == app.FILE_QUESTION_MARK_HANDLER:
                if question_number == 0:
                    question_quiz.question += "#{0}\n\n".format(app.BOT_MESSAGE_SEARCH_TAG)
                    question_quiz.question += fileline[3:]

                    break
                else:
                    question_number -= 1

        for fileline in file:
            """Получаем дополнительный контент вопроса (с отступами). Выходим при переходе на ответ."""
            if fileline[0:3] == app.FILE_ANSWER_MARK_HANDLER:
                question_quiz.options.append(fileline[3:])

                break

            question_quiz.question += fileline

        for fileline in file:
            """Получение ответов. Остановка на новом вопросе."""
            if fileline[0:3] == app.FILE_QUESTION_MARK_HANDLER:
                break
            elif fileline[3:] != '':
                question_quiz.options.append(fileline[3:])

    return question_quiz


def get_amount_questions(app):
    """Получение общего количества вопросов в файле"""
    amount_questions = 0

    with open(app.FILE_QUESTION_NAME, 'r') as file:
        for fileline in file:
            if fileline[0:3] == app.FILE_QUESTION_MARK_HANDLER:
                amount_questions += 1

    return amount_questions


def get_question_number(app):
    """
    Определение текущего вопроса.
    Запись номера вопроса.
    Если вопросы закончились, будет рандом (заглушка).
    Когда появится новый вопрос, он будет вызван как следующий.
    """
    open(app.FILE_QUESTION_COUNTER_NAME, 'a').close()

    with open(app.FILE_QUESTION_COUNTER_NAME, 'r') as file:
        fileline = file.readline()

        counter_question_number = int(fileline) if fileline != '' else 0
        amount_questions = get_amount_questions(app=app)

        if amount_questions > counter_question_number:
            counter_question_number = set_counter_questions(app=app)
        else:
            counter_question_number = random.randrange(start=amount_questions)

        return counter_question_number


def set_counter_questions(app):
    """Запись в счетчик вызванных вопросов. Просто счетчик."""
    question_number = 1
    open(app.FILE_QUESTION_COUNTER_NAME, 'a').close()

    with open(app.FILE_QUESTION_COUNTER_NAME, 'r+') as file:
        fileline = file.readline()

        file.seek(0)

        if fileline != '':
            question_number = int(fileline) + 1

        file.write(str(question_number))
        file.truncate()

    return question_number - 1


def randomize_options(options):
    """Обычная рандомизация ответов с получением корректного ответа"""
    correct_option_id = random.randrange(start=len(options))
    options[0], options[correct_option_id] = options[correct_option_id], options[0]

    return correct_option_id


def main():
    """Функция найдет следующий вопрос и отправит в зарегистрированные группы телеграм"""
    app = kernel.Kernel()
    question_quiz = get_question_quiz(
        app=app,
        question_number=get_question_number(app=app)
    )
    correct_option_id = randomize_options(options=question_quiz.options)

    create_telegram_quiz(
        app=app,
        question=question_quiz.question,
        options=question_quiz.options,
        correct_option_id=correct_option_id,
    )


main()
