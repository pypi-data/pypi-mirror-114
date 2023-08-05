import os
import jwt
import websocket
import configparser
import json
import requests
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

    def sendMessage(self, roomId, message):
        url = "{}/botMessage".format(self.config['wss']['api'])
        headers = {'Content-Type': 'application/json'}
        payload = {"roomId": roomId, "message": message}
        response = requests.request("POST", url, headers=headers, json=payload)
        print('sendMessage',payload, response)
    
    def sendSms(self, userId, message):
        url = "{}/sendSMSFromBot".format(self.config['wss']['api'])
        headers = {'Content-Type': 'application/json'}
        payload = {"userId": userId, "message": message}
        response = requests.request("POST", url, headers=headers, json=payload)
        print('sendSms',payload, response)

    def sendPushNotification(self, roomId, message):
        url = "{}/sendPushNotificationFromBot".format(self.config['wss']['api'])
        headers = {'Content-Type': 'application/json'}
        payload = {"roomId": roomId, "message": message}
        response = requests.request("POST", url, headers=headers, json=payload)
        print('sendPushNotification',payload, response)

    def sendEmail(self, userId, subject, html):
        url = "{}/sendEmailFromBot".format(self.config['wss']['api'])
        headers = {'Content-Type': 'application/json'}
        payload = {"userId": userId, "subject": subject, "html": html}
        response = requests.request("POST", url, headers=headers, json=payload)
        print('sendEmail',payload, response)

    def connect(self):
        token = jwt.encode({"botToken": self.bot_token}, self.bot_token, algorithm="HS256")
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
        config_path = os.path.join(path_current_directory, 'config', 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        self.config = config
        self.bot_token = ''
        self.client_id = ''
        self.wss = {}
        self.ee = EventEmitter()