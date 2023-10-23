import json
import logging
from logging import Logger

from config.constants import NGROK_IP, NGROK_PORT, NGROK_TUNNELS_API
from service.http.http_method import HTTPMethod
from service.http.http_request import HTTPRequest
from service.http.http_response import HTTPResponse
from service.http.http_service import HTTPService


class NgrokService:

    __LOGGER: Logger = logging.getLogger(__name__)

    @classmethod
    def get_tunnel_endpoint(cls, tunnel_name: str) -> str:
        http_request: HTTPRequest = HTTPRequest(
            http_method=HTTPMethod.GET,
            url=f"http://{NGROK_IP}:{NGROK_PORT}/{NGROK_TUNNELS_API}/{tunnel_name}"
        )

        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Requesting tunnel {tunnel_name} info to ngrok endpoint {http_request.url}"
        )

        http_response: HTTPResponse = HTTPService.make_http_request(http_request)

        del http_request

        if http_response.http_code == 400:
            raise NgrokServiceTunnelNotFoundException(f"Tunnel {tunnel_name} doesnt exists in ngrok")
        elif http_response.is_bad_http_request():
            raise NgrokServiceException(
                f"There was a problem retrieving information from tunnel {tunnel_name}. Response {http_response}"
            )

        response: dict = json.loads(
            http_response.response,
        )

        del http_response

        return response["public_url"]


class NgrokServiceException(Exception):
    def __int__(self, msg: str):
        super().__init__(msg)
        self.__msg = msg


class NgrokServiceTunnelNotFoundException(NgrokServiceException):
    def __int__(self, msg: str):
        super().__init__(msg)
        self.__msg = msg
