from dataclasses import dataclass


@dataclass
class ConsoleInfo:
    id: int
    suffix: str
    preferredWidth: int
    genericName: str
