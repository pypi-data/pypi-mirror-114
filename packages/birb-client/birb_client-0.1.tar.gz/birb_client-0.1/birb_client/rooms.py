class Rooms():
    def __init__(self, client) -> None:
        self._client = client

    def list(self):
        return self._client._get('/rooms')

    def create(self):
        return self._client._post('/rooms')