from pathlib import Path

from AM2S.data.GameInfo import GameInfo


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
        return (self.__firstLine
                + self.__secondLine
                + "\n"
                + self.__thirdLine)

    def saveResult(self, path: Path):
        if not path.exists() or path.is_file():
            raise Exception(f"{path} does not exist")
        filePath = path / (self.__info.rom.path.stem + ".txt")
        with open(filePath, "w+") as f:
            f.write(self.getText())
            f.close()

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
