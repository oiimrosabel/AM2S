from requests import get

from AM2S.builders.GameInfoBuilder import GameInfoBuilder
from AM2S.data.GameInfo import GameInfo
from AM2S.data.Identity import Identity
from AM2S.data.RomFile import RomFile
from AM2S.enums.ScreenscraperEndpoint import ScreenscraperEndpoint
from AM2S.interfaces.SCRequester import SCRequester


class InfoRequester(SCRequester[RomFile, GameInfo]):
    def __init__(self, identity: Identity):
        super().__init__(identity, ScreenscraperEndpoint.INFO)

    def getData(self, rom: RomFile) -> GameInfo:
        requestUrl = self.getRequestURL()
        requestUrl.add({
            "crc": rom.hash.crc32,
            "md5": rom.hash.md5,
            "sha1": rom.hash.sha1,
            "systemeid": str(rom.console.id),
            "romtype": "rom",
            # "romnom": rom.path.name,
            "romtaille": str(rom.size)
        })
        res = get(requestUrl.url)
        res.raise_for_status()
        return GameInfoBuilder(res.json(), rom).build()
