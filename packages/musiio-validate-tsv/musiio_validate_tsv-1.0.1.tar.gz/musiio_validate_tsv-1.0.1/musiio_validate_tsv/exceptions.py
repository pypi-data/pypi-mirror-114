class TSVException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TSVInvalidFieldValueError(TSVException):
    def __init__(self, message):
        super().__init__(message)


class TSVInvalidFieldTypeError(TSVException):
    def __init__(self, message):
        super().__init__(message)


class TSVMissingRequiredFieldError(TSVException):
    def __init__(self, message):
        super().__init__(message)


class TSVColumnUnsetError(TSVException):
    def __init__(self, message):
        super().__init__(message)


class TSVInconsistentColumnRowError(TSVException):
    def __init__(self, message):
        super().__init__(message)