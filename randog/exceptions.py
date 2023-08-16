import warnings


class FactoryConstructionError(Exception):
    _message: str

    @property
    def message(self) -> str:
        return self._message

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message


def apply_formatwarning():
    origin_formatwarning = warnings.formatwarning

    def _formatwarning(message, category, *args, **kwargs):
        if issubclass(category, RandogCmdWarning):
            if isinstance(message, Warning):
                return f"warning: {message.args[0]}\n"
            else:
                return f"warning: {message}\n"
        else:
            return origin_formatwarning(message, category, *args, **kwargs)

    warnings.formatwarning = _formatwarning


class RandogCmdWarning(FutureWarning):
    """warning raised during command execution"""

    pass
