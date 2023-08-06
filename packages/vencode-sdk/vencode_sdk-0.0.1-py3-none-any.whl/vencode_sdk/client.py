import json
import sseclient
import time
from . import api
from . import Access, Notify, Credentials, CreateEncodeJobOptions

BASE_URL = 'https://api.vencode.io/api'


class Options:
    def __init__(self, access: Access, notify: Notify = None, baseUrl=BASE_URL, credentials: Credentials = None, debug: bool = False, maxListenRetry: int = 15):
        self.baseUrl = baseUrl
        self.access = access
        self.notify = notify
        self.credentials = credentials
        self.debug = debug
        self.maxListenRetry = maxListenRetry

    def url(self):
        return self.baseUrl


class Client:
    def __init__(self, options: Options):
        self.options = options
        self.listeners = []

    def with_urllib3(self, url):
        try:
            import urllib3
            http = urllib3.PoolManager()

            res = http.request('GET', url, preload_content=False)

            return res
        except Exception:
            pass

    def with_requests(self, url):
        import requests
        return requests.get(url, stream=True)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def encode(self, encode: CreateEncodeJobOptions):
        return api.post(self, "/jobs", json={'credentials': self.options.credentials.toJson(), **encode.toJson()})

    def stop_job(self, id):
        return api.post(self, f"/jobs/{id}/cancel")

    def get_job_metadata(self, id):
        return api.get(self, f"/jobs/{id}")

    def listen_all(self, callback):
        self.listen('ALL', callback=callback)

    def listen(self, id, callback):
        id_entry = "all=true" if id == 'ALL' else f'id={id}'

        while 1:
            response = self.with_urllib3(
                self.options.baseUrl + f'/events?{id_entry}&creds={json.dumps(self.options.access, default=lambda o: o.__dict__)}')
            client = sseclient.SSEClient(response)

            for event in client.events():
                callback(event.data)

            time.sleep(60)
