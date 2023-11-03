from http.client import HTTPResponse as httpResponse
from logging import INFO, Logger
import logging

from src.bot.constants import DEFAULT_ENCODING
from src.bot.application.shared.http.http_connector import HTTPConnector, HTTPConnectorException, HTTPConnectorNotFoundException
from src.bot.application.shared.http.http_request import HTTPRequest
from src.bot.application.shared.http.http_response import HTTPResponse


class HTTPService:
    
    __LOGGER: Logger = logging.getLogger(__name__)

    def __int__(self) -> None:
        raise HTTPServiceException("This class cannot be instantiate!!. Only has static methods")

    @classmethod
    def make_http_request(cls, http_request: HTTPRequest) -> HTTPResponse:
        """
        Make a http request and return the response
        :param http_request:
        :return: HTTPRespose

        :raise: HTTPServiceConnectionRefusedException
        """

        cls.__LOGGER.log(
            level=INFO,
            msg=http_request
        )

        response: httpResponse = None
        http_response: HTTPResponse = None
        try:
            response: httpResponse = HTTPConnector.create_http_connection(http_request)
        except HTTPConnectorNotFoundException as e:
            http_response: HTTPResponse = HTTPResponse(
                http_code=400
            )
            return http_response
        except HTTPConnectorException as e:
            raise HTTPServiceConnectionRefusedException from e
            
        http_response: HTTPResponse = HTTPResponse(
            headers=dict(response.headers),
            response=str(response.read(), encoding=DEFAULT_ENCODING),
            http_code=response.status
        )

        HTTPConnector.close_http_connection(response)
        del response

        cls.__LOGGER.log(
            level=INFO,
            msg=http_response
        )

        return http_response


# Class exception
class HTTPServiceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class HTTPServiceConnectionRefusedException(HTTPServiceException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)