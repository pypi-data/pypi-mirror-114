def Logger(message):
    print(message, end="\n")

from enum import Enum

class LoggerType(Enum):
    Error = 1
    Warning = 2
    action = 3
    