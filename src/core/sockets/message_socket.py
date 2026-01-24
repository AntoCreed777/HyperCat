from .type_status import TypeStatus


class MessageSocket:
    @staticmethod
    def create_message(message: str | dict, status_code: TypeStatus) -> dict:

        response = {"status": status_code.name, "message": message}

        return response

    @staticmethod
    def parse_message(response: dict) -> tuple[TypeStatus, str | dict]:
        status_code = TypeStatus[response["status"]]
        message = response["message"]

        return status_code, message
