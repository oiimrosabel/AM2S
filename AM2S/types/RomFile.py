from pathlib import Path

from AM2S.presets.Console import suffixToConsole
from AM2S.types.Console import Console
from AM2S.types.Hasher import Hasher
from AM2S.types.Record import Record


class RomFile(Record):
    path: Path
    hash: Hasher
    console: Console
    size: int

    def __init__(self, path: Path):
        if not (path.exists() and path.is_file()):
            raise Exception(f"The file doesn't exist : {path}")

        console = suffixToConsole.get(path.suffix.lower())
        if console is None:
            raise Exception(f"The file isn't a recognized ROM : {path}")

        self.path = path
        self.console = console
        self.hash = Hasher(path)
        self.size = path.stat().st_size
