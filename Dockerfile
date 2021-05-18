FROM python:slim

RUN groupadd -g 1000 telegramgroup
RUN useradd -l -u 1000 -g telegramgroup telegrambot

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app

USER telegrambot

CMD [ "python", "message_handler.py" ]
