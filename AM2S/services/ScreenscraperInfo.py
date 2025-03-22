from urllib.parse import urlencode

from requests import get

from AM2S.presets.ScreenscraperEndpoint import ScreenscraperEndpoint
from AM2S.services.ScreenscaperRequester import ScreenscraperRequester
from AM2S.types.GameInfo import GameInfo
from AM2S.types.Identity import Identity
from AM2S.types.RomFile import RomFile


class ScreenscraperInfo(ScreenscraperRequester):

    def __init__(self, identity: Identity):
        super().__init__(identity, ScreenscraperEndpoint.INFO)

    def getRomInfo(self, rom: RomFile):
        params = self.getBaseQuery()
        extraParams = {
            "crc": rom.hash.crc32,
            "md5": rom.hash.md5,
            "sha1": rom.hash.sha1,
            "systemeid": str(rom.console.id),
            "romtype": "rom",
            "romnom": rom.path.name,
            "romtaille": str(rom.size)
        }
        params.update(extraParams)
        finalRequestUrl = f"{self.getRequestURL()}?{urlencode(params)}"
        res = get(finalRequestUrl)
        if res.status_code != 200:
            data = {
                "response": {
                    "jeu": {}
                }
            }
        else:
            data = res.json()
        return GameInfo(data, rom)
