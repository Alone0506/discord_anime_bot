# Let Discord bot can run 24hr

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return 'Bot is aLive!'


def run():
    app.run(host="0.0.0.0", port=8060)


def keep_alive():
    server = Thread(target=run)
    server.start()
