from html import unescape

import dpath

from AM2S.types.GameMedia import GameMedia
from AM2S.types.Record import Record
from AM2S.types.RomFile import RomFile


class GameInfo(Record):
    of: RomFile
    releaseDate: str
    nbOfPlayers: str
    editor: str
    synopsis: str
    genres: list[str]
    medias: GameMedia

    def __init__(self, data: dict, of: RomFile):
        self.of = of

        self.releaseDate = self.getReleaseDate(
            list(dpath.get(data, '/response/jeu/dates', default=[])))

        self.nbOfPlayers = self.getNbOfPlayers(
            dict(dpath.get(data, '/response/jeu/joueurs', default=[])))

        self.editor = self.getEditor(
            dict(dpath.get(data, '/response/jeu/editeur', default=[]))
        )

        self.synopsis = self.getSynopsis(
            list(dpath.get(data, '/response/jeu/synopsis', default=[]))
        )

        self.genres = self.getGenres(
            list(dpath.get(data, '/response/jeu/genres', default=[]))
        )

        self.medias = self.getMedias(
            list(dpath.get(data, '/response/jeu/medias', default=[]))
        )

    @staticmethod
    def getReleaseDate(dates: list[dict]):
        default = ""

        if dates is None or dates == []:
            return default

        dates.sort(key=lambda x: x.get("text"))
        return unescape(dates[0].get("text", default))

    @staticmethod
    def getNbOfPlayers(players: dict):
        default = "1"

        if players is None:
            return default

        return unescape(players.get("text", default))

    @staticmethod
    def getEditor(data: dict):
        default = "[no editor]"

        if data is None:
            return default

        return unescape(data.get("text", default))

    @staticmethod
    def getSynopsis(synopsis: list[dict]):
        default = "This game doesn't have any synopsis."

        if synopsis is None or synopsis == []:
            return default

        englishSynopsis = [x for x in synopsis if x.get("langue", "") == "en"]

        if not englishSynopsis:
            return default

        return unescape(englishSynopsis[0].get("text", default))

    @staticmethod
    def getGenres(genres: list[dict]):
        res = []

        if genres is None:
            return res


        for genre in genres:
            names = genre.get("noms", [])
            englishName = [x for x in names if x.get("langue", "") == "en"]
            if len(englishName) > 0:
                res.append(unescape(englishName[0].get("text")))
        print(res)
        return res

    def getMedias(self, data: list[dict]):
        return GameMedia(data, self.of)
