import requests
from requests.exceptions import HTTPError


class ArxConnectionError(Exception):
    """
    Arx Repository is not reachable.
    """


class ArxInternalError(Exception):
    """
    Uh-oh! This should not be raised.
    """


class Arx:
    REPOSITORY_URI = "http://localhost:7777"
    DEFAULT_NAMESPACE = "default"
    CACHE = {}

    def __init__(self, uri=None):
        if uri:
            self.REPOSITORY_URI = uri.rstrip("/")

    def get(self, key=None, default=None, namespace=None):
        if namespace is None:
            namespace = self.DEFAULT_NAMESPACE

        query_url = f"{self.REPOSITORY_URI}/api/v1/{namespace}/"
        single = False
        if key is not None:
            single = True
            query_url += f"{key}/"

        try:
            resp = requests.get(query_url)
            resp.raise_for_status()
            if single:
                return resp.json()["value"]
            return resp.json()["variables"]
        except HTTPError as exc:
            # print(exc.response.text)
            if exc.response.status_code == 404:
                return default
            raise ArxConnectionError(
                f"A connection could not be created to {self.REPOSITORY_URI}"
            )
        except Exception:
            raise ArxInternalError

    def __getattr__(self, key):
        return self.get(key)

    def __getitem__(self, key):
        return self.get(key)
