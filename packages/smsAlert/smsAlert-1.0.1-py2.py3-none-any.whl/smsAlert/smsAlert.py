# -*- coding: utf-8 -*-

import json
import requests


class smsAlertException(Exception):

    def __init__(self, message):
        self.message = message

    def get_message(self):
        return self.message


class smsAlertMsg(object):
    """A simple Python API for the smsAlert

    It includes methods for calling sms api of smsAlert
    """

    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password

        self.sms_url = 'http://smsalert.co.in/api/push.json?'


    def send_sms(self,mobileno, message, senderid, route):
        res = requests.get(self.sms_url,
                           params={'user': self.username,
                                   'pwd': self.password,
                                   'mobileno': mobileno,
                                   'text': message,
                                   'sender': senderid,
                                   'route': route,
                                   'response': 'json'})
        return json.loads(res.content)
    