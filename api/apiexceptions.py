import datetime
import settings
from flask import jsonify

class ApiException(Exception):
    status: int = 500
    details = None
    code: str = None
    date: datetime.datetime
    message: str
    innerException: BaseException = None

    def __init__(self, message: str, status: int = None, code: str = None, details=None,
                 innerException: BaseException = None):
        Exception.__init__(self)
        self.message = message
        if status is not None:
            self.status = status
        self.details = details

        if code is not None:
            self.code = code
        self.date = datetime.datetime.now(tz=settings.get_timezone())
        self.innerException = innerException
        pass

    def to_dict(self):
        rv = dict()
        if self.details is not None:
            rv["details"] = self.details
        rv["message"] = self.message
        rv["status"] = self.status
        rv["date"] = self.date.isoformat()
        rv["code"] = self.code
        return rv


class InvalidKeyException(ApiException):
    def __init__(self, message: str = "API Key not valid. Please pass a valid Key", details =None):
        ApiException.__init__(self, message=message, status=403, code="INVALID_KEY", details=details)
        pass


class NotFoundException(ApiException):
    def __init__(self, message: str, code: str = "404", details=None):
        ApiException.__init__(self, message=message, status=404, code=code, details=details)
        pass


def deal_exception(e: Exception):
    try:
        raise e
    except ApiException as error:
        response = jsonify(error.to_dict())
        response.status_code = error.status
    except Exception as error:
        error_new = ApiException(message=str(error),
                                 innerException=error,
                                 code="INTERNAL_ERROR")
        response = jsonify(error_new.to_dict())
        response.status_code = error_new.status
        return response
    pass
