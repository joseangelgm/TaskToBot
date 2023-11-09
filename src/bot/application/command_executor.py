import json


class CommandExecutor:

    # TODO: Raise exception
    def __init__(self) -> None:
        pass

    @classmethod
    def process_message_and_execute_command(cls, request_body: str) -> None:
        
        response_json: dict = json.loads(request_body)

        # Check if user has permission to execute the command
