from http.client import HTTPResponse
from urllib.request import Request, urlopen
from urllib import parse

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
        http_response: HTTPResponse

        if HTTPMethod.GET == http_request.http_method:
            request: Request = Request(
                url=http_request.url,
                method=http_request.http_method.value,
                headers=http_request.headers,
            )
            http_response = urlopen(request)
        else: # POST
            if http_request.body is {}:
                post_data = parse.urlencode(http_request.body).encode(encoding=DEFAULT_ENCODING)

                request: Request = Request(
                    url=http_request.url,
                    method=http_request.http_method.value,
                    headers=http_request.headers,
                )
                http_response = urlopen(request, data=post_data)
            else:
                request: Request = Request(
                    url=http_request.url,
                    method=http_request.http_method.value,
                    headers=http_request.headers,
                )
                http_response = urlopen(request)

        return http_response

    @staticmethod
    def close_http_connection(http_response: HTTPResponse) -> None:
        http_response.close()


class HTTPConnectorException(Exception):
    def __int__(self, msg: str):
        super().__init__(msg)
        self.__msg = msg
