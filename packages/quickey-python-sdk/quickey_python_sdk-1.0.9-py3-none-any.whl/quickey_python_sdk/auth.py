from quickey_python_sdk.config import base_url
import requests

class Auth:
    def __init__(self, apiKey):
        self.__apiKey = apiKey,
    
    def getAccessToken(self, email, phone, provider):
        headers = {'authorization':self.__apiKey}
        payload = {'email':email, 'phone':phone, 'provider':provider}
        return requests.post('{0}/loginCustomer'.format(base_url), data=payload, headers=str(headers))

    def linkPhoneToEmail(self, phone, token):
        self.__phone = phone
        self.__token = token
        headers = {'authorization':self.__apiKey}
        payload = {'phone':self.__phone, 'token':self.__token}
        return requests.post('{0}/otp/linkToEmail'.format(base_url), data=payload, headers=str(headers))
