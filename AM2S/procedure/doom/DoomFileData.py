from dataclasses import dataclass
from pathlib import Path


@dataclass
class DoomFileData:
    parentWad: Path
    dehFiles: dict[int, Path]
    wadFiles: dict[int, Path]
    lastDeh: Path | None
    lastWad: Path | None
