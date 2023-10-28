from http.client import HTTPResponse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib import parse

from config.constants import DEFAULT_ENCODING
from src.application.service.http.http_method import HTTPMethod
from src.application.service.http.http_request import HTTPRequest


class HTTPConnector:

    def __int__(self) -> None:
        raise HTTPConnectorException("This class cannot be instantiate!!. Only has static methods")

    @staticmethod
    def create_http_connection(http_request: HTTPRequest) -> HTTPResponse:
        """
        create and http connection
        :param http_request:
        :return: HTTPResponse

        :raise: HTTPConnectorException if connection refused or the service is not running
        :raise: HTTPConnectorNotFoundException if http request returns 400
        """

        request: Request = None
        http_response: HTTPResponse = None

        try:
            if HTTPMethod.GET == http_request.http_method:
                request: Request = Request(
                    url=http_request.url,
                    method=http_request.http_method.value,
                    headers=http_request.headers,
                )
                http_response = urlopen(request)
            else: # POST
                if http_request.body is {}:
                    request: Request = Request(
                        url=http_request.url,
                        method=http_request.http_method.value,
                        headers=http_request.headers,
                    )
                    http_response = urlopen(request)
                else:
                    post_data: bytes = parse.urlencode(http_request.body).encode(encoding=DEFAULT_ENCODING)

                    request: Request = Request(
                        url=http_request.url,
                        method=http_request.http_method.value,
                        headers=http_request.headers,
                    )
                    http_response = urlopen(request, data=post_data)
        except HTTPError as e:
            raise HTTPConnectorNotFoundException(e) from e
        except URLError as e:
            raise HTTPConnectorException(e) from e

        return http_response

    @staticmethod
    def close_http_connection(http_response: HTTPResponse) -> None:
        http_response.close()


class HTTPConnectorException(Exception):
    def __int__(self, msg: str):
        super().__init__(msg)
        self.__msg = msg

class HTTPConnectorNotFoundException(HTTPConnectorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)