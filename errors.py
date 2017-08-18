class BadCommandSyntaxError(Exception):
    pass


class IncorrectArgumentTypeError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class NotInActiveVoiceChannelError(Exception):
    pass
