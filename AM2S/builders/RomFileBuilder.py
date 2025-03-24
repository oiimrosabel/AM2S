from pathlib import Path

from AM2S.builders.HashesBuilder import HashesBuilder
from AM2S.data.ConsoleInfo import ConsoleInfo
from AM2S.data.RomFile import RomFile
from AM2S.enums.BoxSizes import BoxSizes
from AM2S.interfaces.Builder import Builder

consoleList = [
    ConsoleInfo(135, ".wad", BoxSizes.MID, "Doom"),
    ConsoleInfo(9, ".gb", BoxSizes.MID, "Nintendo Game Boy"),
    ConsoleInfo(12, ".gba", BoxSizes.WIDE, "Nintendo Game Boy Advance"),
    ConsoleInfo(10, ".gbc", BoxSizes.MID, "Nintendo Game Boy Color"),
    ConsoleInfo(3, ".nes", BoxSizes.MID, "Nintendo NES-Famicom"),
    ConsoleInfo(4, ".sfc", BoxSizes.WIDE, "Nintendo SNES-SFC"),
    ConsoleInfo(234, ".p8", BoxSizes.MID, "PICO-8"),
    ConsoleInfo(19, ".32x", BoxSizes.WIDE, "Sega 32X"),
    ConsoleInfo(2, ".sms", BoxSizes.WIDE, "Sega Master System"),
    ConsoleInfo(20, ".chd", BoxSizes.MID, "Sega Mega CD - Sega CD"),
    ConsoleInfo(1, ".md", BoxSizes.WIDE, "Sega Mega Drive - Genesis"),
    ConsoleInfo(138, ".sh", BoxSizes.MID, "External - Ports")
]

suffixToConsole = {c.suffix: c for c in consoleList}


class RomFileBuilder(Builder[RomFile]):
    __path: Path
    __console: ConsoleInfo

    def __init__(self, path: Path):
        if not (path.exists() and path.is_file()):
            raise Exception(f"The file doesn't exist : {path}")

        console = suffixToConsole.get(path.suffix.lower())
        if console is None:
            raise Exception(f"The file isn't a recognized ROM : {path}")

        self.__console = console
        self.__path = path

    def build(self) -> RomFile:
        return RomFile(
            path=self.__path,
            hash=HashesBuilder(self.__path).build(),
            console=self.__console,
            size=self.__path.stat().st_size
        )
