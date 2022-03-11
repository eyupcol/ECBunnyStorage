from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from io import BytesIO
import requests


@deconstructible
class ECBunnyDjangoStorage(Storage):
    def __init__(self, path=None, access_key=None):
        if not path:
            self.path = str(settings.MEDIA_ROOT)
        if not access_key:
            self.access_key = settings.ACCESS_KEY
        self.cdn = settings.MEDIA_URL

        self.headers = {"Accept": "*/*", "AccessKey": self.access_key}

    def _open(self, name, mode='rb'):
        try:
            url = self.path + name
            response = requests.request("GET", url, headers=self.headers)
            with BytesIO(response.content) as file_content:
                return file_content
        except:
            pass

    def _save(self, name, content):
        try:
            requests.request("PUT", self.path + name, data=content, headers=self.headers)
            return name
        except:
            pass

    def delete(self, name):
        try:
            if not self.exists(name):
                return
            requests.request("DELETE", self.path + name, headers=self.headers)
        except:
            pass

    def listdir(self):
        pass

    def exists(self, name):
        req = requests.head(self.cdn + name)
        return req.status_code == requests.codes.ok

    def size(self):
        pass

    def url(self, name):
        return self.cdn + name
