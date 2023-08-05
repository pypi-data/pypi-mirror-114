import os
import jwt
import websocket
import configparser
import json

from pymitter import EventEmitter


class Client:
    def on_open(self, ws):
        self.ee.emit("open")

    def on_message(self, ws, message):
        message_parse = json.loads(message)
        if message_parse['type'] == 'command':
            self.ee.emit("command", message_parse['data'])

        if message_parse['type'] == 'setting':
            self.ee.emit("setting", message_parse['data'])

    def on_error(self, ws, error):
        self.ee.emit("error", error)

    def on_close(self, ws):
        self.ee.emit("close")

    def connect(self):
        token = jwt.encode({"bot_token": self.bot_token}, self.bot_token, algorithm="HS256")
        wss_url = "{}?token={}&clientId={}".format(self.config['wss']['url'], token, self.client_id)
        self.wss = websocket.WebSocketApp(wss_url, on_open=self.on_open,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close)
        self.wss.run_forever()

    def login(self, bot_token, client_id):
        self.bot_token = bot_token
        self.client_id = client_id
        self.connect()

    def __init__(self):
        path_current_directory = os.path.dirname(__file__)
        # config_path = os.path.join(path_current_directory, 'config', 'config.ini')
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'config', 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        self.config = config
        self.bot_token = ''
        self.client_id = ''
        self.wss = {}
        self.ee = EventEmitter()
