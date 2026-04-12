class TMSException(Exception):
    pass


class UserNotFoundException(TMSException):
    pass


class AccountNotFoundException(TMSException):
    pass


class InsufficientBalanceException(TMSException):
    pass


class InvalidStateTransitionException(TMSException):
    pass


class ValidationException(TMSException):
    pass
