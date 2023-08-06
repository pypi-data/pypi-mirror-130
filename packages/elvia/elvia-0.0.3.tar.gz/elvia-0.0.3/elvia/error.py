class ElviaException(Exception):
    def __init__(self, message, status_code, headers, body):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return self.message + " " + str(self.status_code) + " " + self.body


class AuthError(ElviaException):
    pass


class InvalidRequestBody(ElviaException):
    pass


class UnexpectedError(ElviaException):
    pass
