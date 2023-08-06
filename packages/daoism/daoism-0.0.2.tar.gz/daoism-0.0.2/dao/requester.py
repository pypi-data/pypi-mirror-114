from .model import BaseAPIModel, TransModel, OcrModel
from .auth import Auth
import httpx


class OnlyOneQueryException(Exception):
    pass


class EmpetyQueryException(Exception):
    pass


class Connector:

    model: BaseAPIModel

    def __init__(self, key, secret) -> None:
        # TODO pass a config to override model.config
        self.data = {}
        self.data.update(self.model.config)
        self.auth = Auth(key=key, secret=secret)

    def _build_data(self, **kwargs):
        # Very stupid way to check whether q or img exist
        keys = kwargs.keys()
        if len(keys) > 1:
            raise OnlyOneQueryException("No! Only one query")
        if not kwargs:
            raise EmpetyQueryException("Must have a query to pass")
        # q = list(kwargs.items())[0][1]
        q = list(kwargs.values())[0]
        self.data.update(kwargs)
        self.data.update(self.auth.get_auth(q))
        # print(self.data)

    def sync_connect(self, **kwargs) -> httpx.Response:
        self._build_data(**kwargs)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        result = httpx.post(self.model.API, data=self.data, headers=headers)
        return result

    async def async_connect(self, **kwargs) -> httpx.Response:
        # Confused about async loop here
        self._build_data(**kwargs)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient() as client:
            result = await client.post(self.model.API, data=self.data, headers=headers)
            return result

    def stream(self):
        pass


class TranslateConnector(Connector):
    model = TransModel()

    def search(self, q):
        result = self.sync_connect(q=q)
        return result

    async def async_search(self, q):
        result = await self.async_connect(q=q)
        return result


class TextOcrConnector(Connector):
    model = OcrModel()

    def upload(self, img):
        result = self.sync_connect(img=img)
        return result

    async def async_upload(self, img):
        result = await self.async_connect(img=img)
        return result
