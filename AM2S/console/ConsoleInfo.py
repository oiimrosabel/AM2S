from dataclasses import dataclass

from AM2S.procedure import Procedure


@dataclass
class ConsoleInfo:
    id: int
    suffixes: list[str]
    preferredWidth: int
    genericName: str
    procedure: Procedure
