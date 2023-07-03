import urllib.parse
from lxml import html
from typing import Callable, Generator, Optional, Union


class BaseRequest:
    def __init__(self, url: str, callback: Callable[..., Generator[Union['BaseRequest', dict, None], None, None]],
                 method: str = "GET", payload: Optional[dict] = None,
                 headers: Optional[dict] = None, meta: Optional[dict] = None):
        self.url = url
        self.callback = callback
        self.method = method
        self.payload = payload
        self.headers = headers
        self.meta = meta


class BaseResponse:
    def __init__(self, request: BaseRequest, body: str):
        self.request = request
        self.body = body
        self.__root = html.fromstring(body)

    def xpath(self, expr):
        return self.__root.xpath(expr)

    def follow(self, url: str, callback: Callable, method: str = "GET", payload: dict = None, headers: dict = None,
               meta: dict = None) -> BaseRequest:

        if not self.is_vaild_url(url):
            url = urllib.parse.urljoin(self.request.url, url)

        return BaseRequest(url, callback, method, payload, headers, meta)

    @property
    def meta(self):
        return self.request.meta

    @staticmethod
    def is_vaild_url(url: str) -> bool:
        result = urllib.parse.urlparse(url)
        if result.scheme and result.netloc:
            return True
        else:
            return False
