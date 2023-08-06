from dataclasses import dataclass
from .requester import TranslateConnector, TextOcrConnector


@dataclass
class YouDao:
    key: str
    secret: str

    def translator(self):
        return TranslateConnector(**self.__dict__)

    def ocr(self):
        return TextOcrConnector(**self.__dict__)
