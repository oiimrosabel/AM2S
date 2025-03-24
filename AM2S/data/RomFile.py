from dataclasses import dataclass
from pathlib import Path

from AM2S.data.ConsoleInfo import ConsoleInfo
from AM2S.data.Hashes import Hashes


@dataclass
class RomFile:
    path: Path
    hash: Hashes
    console: ConsoleInfo
    size: int
