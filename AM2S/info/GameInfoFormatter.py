from pathlib import Path
from time import localtime, strftime

from AM2S.info.GameInfo import GameInfo
from AM2S.misc.NodeTools import NodeTools as Nt


class GameInfoFormatter:
    __info: GameInfo
    __firstLine: str
    __secondLine: str
    __thirdLine: str

    def __init__(self, info: GameInfo):
        self.__info = info

        self.__firstLine = self.__formatFirstLine()
        self.__secondLine = self.__formatSecondLine()
        self.__thirdLine = self.__info.synopsis

    def getText(self) -> str:
        match (self.__firstLine, self.__secondLine, self.__thirdLine):
            case ("", "", ""):
                return self.__getFallbackText()
            case ("", "", desc):
                return desc
            case (stats, tags, desc):
                return f"{stats}{tags}\n{desc}"
            case _:
                raise NotImplementedError()

    def saveText(self, path: Path):
        path = Nt.getFolder(path)

        filePath = path / f"{self.__info.rom.name}.txt"
        with open(filePath, "w") as f:
            f.write(self.getText())
            f.close()

    def __getFallbackText(self):
        t = " " * 4
        return (
                "No info is available for this game. "
                + "Note that this may happen if the ROM is a ROM hack or a homebrew. "
                + "If you know more about this game, please go on https://screenscraper.fr. "
                + "Any help is welcome !\n"
                + "\n"
                + "Here's some useful info :\n"
                + f"{t}- File name : {self.__info.rom.path.name}\n"
                + f"{t}- Console : {self.__info.rom.console.genericName}\n"
                + f"{t}- File size : {self.__info.rom.size} bytes\n"
                + "\n"
                + f"{t}- CRC32 : {self.__info.rom.hash.crc32}\n"
                + f"{t}- SHA1 : {self.__info.rom.hash.sha1}\n"
                + f"{t}- MD5 : {self.__info.rom.hash.md5}\n"
                + "\n"
                + f"Last update : {strftime("%d/%m/%Y %H:%M", localtime())}"
        )

    def __formatFirstLine(self):
        editor = None
        if self.__info.editor != "":
            editor = self.__info.editor

        releaseDate = None
        if self.__info.releaseDate != "":
            releaseDate = self.__info.releaseDate[:4]

        nbPlayers = None
        nb = self.__info.nbOfPlayers
        if nb != "":
            nbPlayers = f"{" to ".join(nb.split("-"))} player{"s" * (nb[-1] != "1")}"

        match (editor, releaseDate, nbPlayers):
            case (None, None, None):
                return ""
            case (v, None, None) | (None, v, None) | (None, None, v):
                return f"{v}\n"
            case (v1, v2, None):
                return f"{v1}, {v2}\n"
            case (v1, None, v2) | (None, v1, v2):
                return f"{v1} - {v2}\n"
            case (v1, v2, v3):
                return f"{v1}, {v2} - {v3}\n"

    @staticmethod
    def __toHashTag(text: str):
        if len(text) == 0:
            return text
        nestedGenre = text.split("/")[-1]
        formatedGenre = (nestedGenre
                         .replace("-", " ")
                         .replace("_", " ")
                         .replace("&", "N"))
        words = formatedGenre.split()
        head = words[0].lower()
        tail = ''.join([i.lower().capitalize() for i in words[1:]])
        return f"#{head}{tail}"

    def __formatSecondLine(self):
        genres = self.__info.genres
        default = ""
        if genres is None or genres == []:
            return default
        allGenres = []
        for genre in genres:
            multiGenre = genre.split(",")
            for mGenre in multiGenre:
                allGenres.append(
                    GameInfoFormatter.__toHashTag(
                        mGenre.strip()))
        return " ".join(list(set(allGenres))) + "\n"
