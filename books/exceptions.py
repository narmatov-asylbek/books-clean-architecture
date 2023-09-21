class BookException(Exception):
    _message = "Error happened"

    def __init__(self, message: str = _message):
        self.message = message


class AlreadyExistsException(BookException):
    _message = "Уже существует"
