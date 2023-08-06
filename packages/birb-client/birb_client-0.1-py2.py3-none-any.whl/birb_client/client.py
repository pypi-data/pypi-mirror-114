import requests
from requests.auth import HTTPBasicAuth
from .rooms import Rooms

class Client():
    def __init__(self, host=None, port=None, username=None, password=None, token=None, secure=False) -> None:
        if not token and not (username and password):
            raise Exception("Birb Client needs either token or username/password for authentication")
        if not host:
            host='localhost'
        if not port:
            port=8080
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._token = token
        self._secure = secure
        self._url = None
        self._requests_session = None
        self._headers = None
        self.rooms = Rooms(self)

    def _get(self, endpoint):
        response = self._session.get('{}{}'.format(self.url, endpoint))
        response.raise_for_status()
        return response.json()
        
    def _post(self, endpoint):
        response = self._session.post('{}{}'.format(self.url, endpoint))
        response.raise_for_status()
        return response.json()

    @property
    def token(self):
        if not self._token:
            self._set_token()
        return self._token

    @property
    def url(self):
        if not self._url:
            self._url = "http"
            if self._secure:
                self.url += "s"
            self._url += "://{}:{}".format(self.host, self.port)
        return self._url

    @property
    def _session(self):
        if not self._requests_session:
            self._requests_session = requests.Session()
        if not self._headers:
            self._set_headers()
            self._session.headers.update(self._headers)
        return self._requests_session


    def _set_token(self):
        if not (self.username and self.password):
            raise Exception("Cannot retrieve token without username and password")
        temp_session = requests.Session()
        temp_session.auth = (self.username, self.password)
        response = temp_session.post('{}/login'.format(self.url))
        response.raise_for_status()
        self._token = response.json().get('access_token')

    def _set_headers(self):
        self._headers = dict()
        self._headers['Content-Type'] = 'application/json'
        self._headers['Authorization'] = 'Bearer {}'.format(self.token)
        
