from enum import StrEnum


class TerminalColor(StrEnum):
    DEFAULT = "\033[0m"
    TASK = "\033[95m"
    INFO = "\033[94m"
    WARNING = "\033[93m"
    ERROR = "\033[31m"
    SUCCESS = "\033[32m"
    ASK = "\033[36m"


def colorText(text: str, color: TerminalColor):
    return f"{color}{text}{TerminalColor.DEFAULT}"
