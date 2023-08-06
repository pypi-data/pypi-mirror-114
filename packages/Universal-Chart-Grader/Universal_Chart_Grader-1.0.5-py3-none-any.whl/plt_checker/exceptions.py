class CheckerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.debug_info = None


class CheckerError(RuntimeError):
    pass


class UCMConversionFailure(CheckerError):
    def __init__(self):
        super().__init__("Conversion failure")


class StudentError(CheckerException):
    def __init__(self):
        super().__init__("Call to student's method raised exception")