from os import makedirs
from pathlib import Path

from AM2S.types.GameInfo import GameInfo


class GameInfoFormatter:
    result: str
    of: GameInfo

    def __init__(self, info: GameInfo):
        self.of = info

        releaseDate = self.formatReleaseDate(info.releaseDate)
        nbOfPlayers = self.formatNbOfPlayers(info.nbOfPlayers)
        editor = self.formatEditor(info.editor)
        genres = self.formatGenres(info.genres)
        synopsis = self.formatSynopsis(info.synopsis)

        self.result = (
                f"{editor}, {releaseDate} - {nbOfPlayers}\n" +
                f"{genres}\n" +
                f"{synopsis}"
        )

    @staticmethod
    def formatReleaseDate(date: str):
        if date == "":
            return "[no date]"
        return date[:4]

    @staticmethod
    def formatNbOfPlayers(nb: str):
        formatedNb = " to ".join(nb.split("-"))
        return f"{formatedNb} player{"s" * (nb[-1] != "1")}"

    @staticmethod
    def formatEditor(editor: str):
        return editor

    @staticmethod
    def formatGenre(text: str):
        if len(text) == 0:
            return text

        nestedGenre = text.split("/")[-1]

        formatedGenre = (nestedGenre.replace("-", " ")
                         .replace("_", " ")
                         .replace("&", "N"))

        genreWords = formatedGenre.split()
        return ("#"
                + genreWords[0].lower()
                + ''.join(
                    [i.lower().capitalize() for i in genreWords[1:]]
                ))

    @staticmethod
    def formatGenres(genres: list[str]):
        default = ""
        if genres is None or genres == []:
            return default

        allGenres = []

        for genre in genres:
            multiGenre = genre.split(",")
            for mGenre in multiGenre:
                allGenres.append(
                    GameInfoFormatter.formatGenre(mGenre.strip())
                )
        return " ".join(list(set(allGenres))) + "\n"

    @staticmethod
    def formatSynopsis(synopsis: str):
        return synopsis

    def saveResult(self, path: Path):
        if path.exists() and not path.is_dir():
            raise Exception("This file is invalid")
        if not path.exists():
            makedirs(path)
        filePath = path / (self.of.of.path.stem + ".txt")
        with open(filePath, "w+") as f:
            f.write(self.result)
            f.close()
