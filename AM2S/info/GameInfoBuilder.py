from html import unescape

import dpath

from AM2S.info.GameInfo import GameInfo
from AM2S.media.GameMediaBuilder import GameMediaBuilder
from AM2S.rom.RomFile import RomFile
from AM2S.templates.Builder import Builder


class GameInfoBuilder(Builder[GameInfo]):
    __rom: RomFile
    __data: dict
    __lang: str
    __regions: list[str]

    def __init__(self, data: dict, rom: RomFile, language="en", regions=[]):
        self.__rom = rom
        self.__data = data
        self.__lang = language
        self.__regions = regions

    def build(self) -> GameInfo:
        return GameInfo(
            rom=self.__rom,
            releaseDate=self.getReleaseDate(),
            nbOfPlayers=self.getNbOfPlayers(),
            editor=self.getEditor(),
            synopsis=self.getSynopsis(),
            genres=self.getGenres(),
            medias=self.getMedias()
        )

    def getReleaseDate(self):
        dates = list(dpath.get(self.__data, '/response/jeu/dates', default=[]))
        default = ""
        if dates is None or dates == []:
            return default
        dates.sort(key=lambda x: x.get("text"))
        return unescape(dates[0].get("text", default))

    def getNbOfPlayers(self):
        players = dict(dpath.get(self.__data, '/response/jeu/joueurs', default=[]))
        default = ""
        if players is None:
            return default
        return unescape(players.get("text", default))

    def getEditor(self):
        editor = dict(dpath.get(self.__data, '/response/jeu/editeur', default=[]))
        default = ""
        if editor is None:
            return default

        return unescape(editor.get("text", default))

    def getSynopsis(self):
        synopsis = list(dpath.get(self.__data, '/response/jeu/synopsis', default=[]))
        default = ""
        if synopsis is None or synopsis == []:
            return default
        englishSynopsis = [x for x in synopsis if x.get("langue", "") == "en"]
        if not englishSynopsis:
            return default
        return unescape(englishSynopsis[0].get("text", default))

    def getGenres(self):
        genres = list(dpath.get(self.__data, '/response/jeu/genres', default=[]))
        res = []
        if genres is None:
            return res
        for genre in genres:
            names = genre.get("noms", [])
            englishName = [x for x in names if x.get("langue", "") == "en"]
            if len(englishName) > 0:
                res.append(unescape(englishName[0].get("text")))
        return res

    def getMedias(self):
        medias = list(dpath.get(self.__data, '/response/jeu/medias', default=[]))
        return GameMediaBuilder(medias, self.__rom).build()
