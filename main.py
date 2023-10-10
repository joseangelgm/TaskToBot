from urllib.request import urlopen, Request

from service.http.http_method import HTTPMethod
from service.http.http_request import HTTPRequest
from service.http.http_response import HTTPResponse
from service.http.http_service import HTTPService


def urllib_example():
    endpoint: str = "https://mocki.io/v1/d4867d8b-b5d5-4a48-a4ab-79131b5809b8"

    request = Request(endpoint, headers={})
    response = urlopen(request)
    print(response.read())
    response.close()


def using_http_service():
    http_request: HTTPRequest = HTTPRequest(
        url="https://mocki.io/v1/d4867d8b-b5d5-4a48-a4ab-79131b5809b8",
        http_method=HTTPMethod.GET,
    )

    http_response: HTTPResponse = HTTPService.make_http_request(http_request=http_request)

    print(http_response)


if __name__ == "__main__":
    # Check python version 3.9
    #urllib_example()
    using_http_service()
