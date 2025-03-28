from requests import get

from AM2S.api.Requester import Requester
from AM2S.api.RequesterEndpoint import RequesterEndpoint
from AM2S.identity.IdentityBuilder import IdentityBuilder
from AM2S.info.GameInfo import GameInfo
from AM2S.info.GameInfoBuilder import GameInfoBuilder
from AM2S.misc.TomlLoader import TomlLoader
from AM2S.rom.RomFile import RomFile


class InfoRequester(Requester[RomFile, GameInfo]):
    __config: TomlLoader

    def __init__(self, config: TomlLoader):
        identity = IdentityBuilder(config).build()
        super().__init__(identity, RequesterEndpoint.INFO)
        self.__config = config

    def getData(self, rom: RomFile) -> GameInfo:
        requestUrl = self.getRequestURL()
        requestUrl.add({
            "crc": rom.hash.crc32,
            "md5": rom.hash.md5,
            "sha1": rom.hash.sha1,
            "systemeid": str(rom.console.id),
            "romtype": "rom",
            "romnom": rom.path.name,
            "romtaille": str(rom.size)
        })
        res = get(requestUrl.url)
        data = {}
        if res.status_code == 200:
            data = res.json()

        language = self.__config.get("scan/language", "en")
        regions = self.__config.get("scan/regions", [])

        return GameInfoBuilder(
            data=data,
            rom=rom,
            language=language,
            regions=regions
        ).build()
