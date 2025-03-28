from dataclasses import dataclass
from pathlib import Path

from AM2S.console.ConsoleInfo import ConsoleInfo
from AM2S.rom.RomFile import RomFile


@dataclass
class RomSet:
    root: Path

    textPath: Path
    previewPath: Path
    boxPath: Path

    console: ConsoleInfo
    games: list[RomFile]
