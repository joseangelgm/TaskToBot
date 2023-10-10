from http.client import HTTPResponse
from urllib.request import Request, urlopen

from config.constants import DEFAULT_ENCODING
from service.http.http_method import HTTPMethod
from service.http.http_request import HTTPRequest


class HTTPConnector:
    def __int__(self):
        raise HTTPConnectorException("This class cannot be instantiate!!. Only has static methods")

    @staticmethod
    def create_http_connection(http_request: HTTPRequest) -> HTTPResponse:
        """
        create and http connection
        :param http_request:
        :return:
        """

        request: Request

        if HTTPMethod.GET == http_request.http_method:
            request: Request = Request(
                url=http_request.url,
                method=http_request.http_method.value,
                headers=http_request.headers,
            )
        else:
            request: Request = Request(
                url=http_request.url,
                method=http_request.http_method.value,
                headers=http_request.headers,
                data=bytes(http_request.body, DEFAULT_ENCODING)
            )

        return urlopen(request)


class HTTPConnectorException(Exception):
    def __int__(self, msg: str):
        self.__msg = msg
        super().__init__(self.__msg)
