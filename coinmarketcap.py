from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from utils.jsonConfig import JsonConfig

class DataRequest():

    def __init__(self, begin = True, start = None, limit = None, convert = None):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.params = {
            "start" : "1",
            "limit" : "5000",
            "convert" : "USD"
        }
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY" : "1a26abb7-8b14-4dda-8c06-add06e8a1186"
        }
        self.data = None
        self.session = None
        if begin:
            self.json = self.requestData(start, limit, convert)
        else:
            self.json = {}

    def requestData(self, start, limit, convert):
        if start is not None:
            self.params["start"] = str(start)
        if limit is not None:
            self.params["limit"] = str(limit)
        self.session = self._createSession()
        self.data = self._requestSnapshot()
        if self.data:
            print("Data loaded")
        return JsonConfig(self.data)

    
    def _createSession(self):
        session = Session()
        session.headers.update(self.headers)
        return session

    def _requestSnapshot(self):    
        try:
            response = self.session.get(self.url, params = self.params)
            return json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def getData(self):
        return self.json