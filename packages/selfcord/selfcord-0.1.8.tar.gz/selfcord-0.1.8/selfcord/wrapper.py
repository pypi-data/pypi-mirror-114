"""
COPYRIGHT BENNY 2021

ALL RIGHTS RESERVED TO THE 
DEVELOPER OF THIS PROJECT.
"""

import requests
import json

__baseUrl = ""
__userToken = ""
__userAgent = ""
__logging = None

class Wrapper:
    def setup(token, baseUrl, userAgent, logging):
        global __userToken, __baseUrl, __userAgent, __logging
        __baseUrl = baseUrl
        __userToken = token
        __userAgent = userAgent
        __logging = logging

    def sendRequest(method, url, headers, payload):
        return requests.request(method=method, url=url, headers=headers, data=str(payload))
    def sendDiscordRequestCustomToken(method, urlAddon, headers, payload, token):
        headers["Authorization"] = token;headers["Content-Type"] = "application/json";headers["User-Agent"] = __userAgent
        if __logging:
            print(json.dumps(headers))
        if method.lower() == "get":
            request = requests.get(__baseUrl + urlAddon, headers=headers)
        else:
            request = requests.request(method, __baseUrl + urlAddon, headers=headers, data=json.dumps(payload))
        return request        
    def sendDiscordRequest(method, urlAddon, headers, payload):
        headers["Authorization"] = __userToken;headers["Content-Type"] = "application/json";headers["User-Agent"] = __userAgent
        if __logging:
            print(json.dumps(headers))        
        if method.lower() == "get":
            request = requests.get(__baseUrl + urlAddon, headers=headers)
        else:
            request = requests.request(method, __baseUrl + urlAddon, headers=headers, data=json.dumps(payload))
        return request
    def getBaseUrl():
        global __baseUrl
        return __baseUrl
    def getUserToken():
        global __userToken
        return __userToken
    def getUserAgent():
        global __userAgent
        return __userAgent
    def getLogging():
        global __logging
        return __logging