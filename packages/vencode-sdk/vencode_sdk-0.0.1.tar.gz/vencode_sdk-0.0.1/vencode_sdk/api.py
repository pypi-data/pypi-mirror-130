import requests


class Error(Exception):
    pass


def apply_headers(client):
    headers = []

    headers = {'User-Agent': 'vencode-sdk/py', 'Content-Type': 'application/json',
               'Accept': 'application/json'}
    headers['x-api-key'] = client.options.access.key
    headers['x-user-id'] = client.options.access.id

    return headers


def get(client, path):
    res = requests.get(path, headers=apply_headers(client))
    return res


def post(client, path, **kwargs):
    res = requests.post(client.options.baseUrl + path,
                        headers=apply_headers(client), json=kwargs.get('json'))
    return res
