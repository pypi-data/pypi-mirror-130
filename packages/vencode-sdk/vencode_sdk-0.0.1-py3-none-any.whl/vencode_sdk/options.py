from typing import List
import json


class Credentials:
    def __init__(
        self,
        clientId: str,
        clientSecret: str,
        type: str,
        bucket=None,
        clientEmail=None,
        region=None,
        projectId=None,
        acl=None,
        endpoint=None
    ):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.type = type
        self.bucket = bucket
        self.clientEmail = clientEmail
        self.region = region
        self.projectId = projectId
        self.acl = acl
        self.endpoint = endpoint

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Notify:
    def __init__(self, webhookUrl: str):
        self.webhookUrl = webhookUrl

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Access:
    def __init__(self, key: str, id: str):
        self.key = key
        self.id = id

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Encode:
    def __init__(self, format, res=None, ac=None, vc=None, asr=None):
        self.res = res
        self.ac = ac
        self.vc = vc
        self.format = format
        self.asr = asr

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Input:
    def __init__(self, path):
        self.path = path

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Output:
    def __init__(self, key, encode: Encode, watermark=None):
        self.key = key
        self.encode = encode
        self.watermark = watermark

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class CreateEncodeJobOptions:
    def __init__(self, input: Input, outputs: List[Output]):
        self.input = input
        self.outputs = outputs

    def toJson(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
