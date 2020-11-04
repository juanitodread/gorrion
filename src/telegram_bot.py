import os

from telegram import Bot, Update


def do_work(event, context) -> dict:
    print('EVENT', event)

    token = os.environ['TELEGRAM_TOKEN']
    print('TOKEN', token)

    bot = Bot(token=token)
    update = Update.de_json(event, bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()

    print(chat_id, msg_id)
    print(text)

    if text == "/start":
        bot_welcome = 'This is the gorrion bot'
        bot.send_message(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    return {
        'status_code': 200,
        'body': {}
    }
