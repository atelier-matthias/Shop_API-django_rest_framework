import requests
from django.conf import settings
import ast
import json


class PayUGatewayCommands(object):

    @classmethod
    def create_order(cls, orderBody):
        url = cls.get_createOrderUrl()
        headers = cls.get_createOrderHeaders()
        data = json.dumps(orderBody)
        res = requests.request('POST', url, headers=headers, data=data)
        # res = requests.post(url, headers=headers, data=data)
        return res

    @classmethod
    def get_createOrderHeaders(cls):
        return {"Content-Type": "application/json", 'Authorization': 'Bearer {}'.format(cls.getToken())}

    @classmethod
    def getToken(cls):
        credentials, headers = cls.get_tokenbody(clientID=settings.PAYU_MERCHANT_KEY, clientSecret=settings.PAY_OAUTH_SECRET)
        token = requests.post(cls.get_tokenUrl(), headers=headers, data=credentials)
        res = ast.literal_eval(token.text)
        return res['access_token']

    @classmethod
    def get_createOrderUrl(cls):
        if settings.PAYU_MODE == "TEST":
            return 'https://secure.snd.payu.com/api/v2_1/orders/'
        if settings.PAYU_MODE == "LIVE":
            return 'https://secure.payu.com/api/v2_1/orders/'
        else:
            return 'https://secure.snd.payu.com/api/v2_1/orders/'

    @classmethod
    def get_tokenUrl(cls):
        if settings.PAYU_MODE == "TEST":
            return 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'
        if settings.PAYU_MODE == "LIVE":
            return 'https://secure.payu.com/pl/standard/user/oauth/authorize'
        else:
            return 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'

    @classmethod
    def get_tokenbody(cls, clientID, clientSecret):
        cred = 'grant_type=client_credentials&client_id={}&client_secret={}'.format(clientID, clientSecret)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return cred, headers
