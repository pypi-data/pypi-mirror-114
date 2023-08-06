from quickey_python_sdk.config import base_url
import requests

class App:
    def __init__(self, apiKey):
        self.__apiKey = apiKey

    def getAppMetaData(self):
        payload = {'apiKey':self.__apiKey}
        return requests.post('{0}/auth/apiKey'.format(base_url), data=payload)

    def sendSMSOTP(self, phone, provider, appId):
        self.__phone = phone
        self.__provider = provider
        self.__appId = appId
        headers = {'authorization':self.__apiKey}
        payload = {'phone':self.__phone, 'provider':self.__provider}
        return requests.post('{0}/getSMSOTP/{1}'.format(base_url, self.__appId), data=payload, headers=str(headers))
