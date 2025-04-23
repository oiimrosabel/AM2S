import re
from pathlib import Path

from AM2S.errors.RomError import RomError
from AM2S.misc.NodeTools import NodeTools as Nt
from AM2S.procedure.doom.DoomFileData import DoomFileData
from AM2S.templates.Builder import Builder


class DoomFileDataBuilder(Builder[DoomFileData]):
    file: Path

    def __init__(self, doomFile: Path):
        self.file = doomFile

    @staticmethod
    def __getKeyAndFile(line: str) -> tuple[str, str]:
        res = re.match("^(\\w*) \"([A-Za-z0-9-._ ]*)\"$", line)
        if res is None:
            raise RomError("Malformed file")
        return res.group(1), res.group(2)

    @staticmethod
    def __getIdFromKey(key: str) -> int:
        keyAndId = key.split("_")
        if len(keyAndId) != 2:
            raise RomError("Malformed file")
        return int(keyAndId[1])

    def build(self) -> DoomFileData:
        wadFolder = f".{self.file.stem}"
        parentWad = None

        dehFiles: dict[int, Path] = {}
        maxDeh = 0

        wadFiles: dict[int, Path] = {}
        maxWad = 0

        doomFile = Nt.getFile(self.file)
        doomFolder = doomFile.parent

        with doomFile.open("r") as f:
            for line in f.readlines():
                key, file = self.__getKeyAndFile(line)
                if file == "":
                    continue
                elif key == "parentwad":
                    parentWad = doomFolder / ".IWAD" / file
                elif key.startswith("dehfile"):
                    fId = self.__getIdFromKey(key)
                    dehFiles[fId] = doomFolder / wadFolder / file
                    maxDeh = max(fId, maxDeh)
                elif key.startswith("wadfile"):
                    fId = self.__getIdFromKey(key)
                    wadFiles[fId] = doomFolder / wadFolder / file
                    maxWad = max(fId, maxWad)
            f.close()

        if parentWad is None:
            raise RomError("Missing parent WAD")

        return DoomFileData(
            parentWad=parentWad,
            dehFiles=dehFiles,
            wadFiles=wadFiles,
            lastWad=wadFiles.get(maxWad),
            lastDeh=dehFiles.get(maxDeh),
        )
