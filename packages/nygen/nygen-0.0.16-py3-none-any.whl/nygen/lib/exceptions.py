class GenException(Exception):
    pass


class BadProjectNameException(GenException):
    pass


class DestinationExistsException(GenException):
    pass


class CondaEnvironmentExistsException(GenException):
    pass


class MissingArgumentException(GenException):
    pass


class CondaException(GenException):
    pass


class TemplateException(GenException):
    pass
