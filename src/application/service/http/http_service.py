from http.client import HTTPResponse as httpResponse

from config.constants import DEFAULT_ENCODING
from src.application.service.http.http_connector import HTTPConnector
from src.application.service.http.http_request import HTTPRequest
from src.application.service.http.http_response import HTTPResponse


class HTTPService:
    def __int__(self):
        raise HTTPServiceException("This class cannot be instantiate!!. Only has static methods")

    @staticmethod
    def make_http_request(http_request: HTTPRequest) -> HTTPResponse:
        """
        Make a http request and return the response
        :param http_request:
        :return:
        """

        response: httpResponse = HTTPConnector.create_http_connection(http_request=http_request)

        http_response: HTTPResponse = HTTPResponse(
            headers=dict(response.headers),
            response=str(response.read(), encoding=DEFAULT_ENCODING),
            http_code=response.status
        )

        HTTPConnector.close_http_connection(response)

        return http_response


# Class exception
class HTTPServiceException(Exception):
    def __int__(self, msg: str):
        super().__init__(msg)
        self.__msg = msg
