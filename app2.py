from os.path import join, dirname
from dotenv import load_dotenv
import os
from flask import Flask, request
import telegram


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращает токен и секретные велечины


TOKEN = get_from_env("TOKEN")
telegram_url = get_from_env("TELEGRAM_URL")
bot = telegram.Bot(token=TOKEN)


def get_response(msg):
    """
    you can place your mastermind AI here
    could be a very basic simple respons
    or a complex LSTM network that generate appropriate answer
    """
    return "TEST"


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '<h1>Hello</h1>'


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id

    # the route here can be anything, you the one who will call it
    @app.route('/setwebhook', methods=['GET', 'POST'])
    def set_webhook():
        # we use the bot object to link the bot to our app which live
        # in the link provided by URL
        s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
        # something to let us know things work
        if s:
            return "webhook setup ok"
        else:
            return "webhook setup failed"

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # here we call our super AI
    response = get_response(text)

    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'


# start the flask app
app = Flask(__name__)


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
