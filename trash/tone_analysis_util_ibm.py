# -*- coding: utf-8 -*-
__author__ = 'Lev'
import requests

IBM_URL = 'https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment'
IBM_KEY = ''

data = dict(text=u'Я ОЧЕНЬ КРУТОЙ', apikey=IBM_KEY, outputMode='json')
response = requests.post(IBM_URL, data)
print(response.text)



