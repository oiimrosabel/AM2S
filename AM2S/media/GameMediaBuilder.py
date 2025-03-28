from furl import furl

from AM2S.media.GameMedia import GameMedia
from AM2S.rom.RomFile import RomFile
from AM2S.templates.Builder import Builder

regions = ["eu", "us", "wor", "jp", "ss"]
basePublicUrl = "https://www.screenscraper.fr/image.php"


class GameMediaBuilder(Builder[GameMedia]):
    __rom: RomFile
    __data: list[dict]

    def __init__(self, data: list[dict], rom: RomFile):
        self.__rom = rom
        self.__data = data

    def build(self) -> GameMedia:
        cartridge = self.getUrlFromData("support-2D")
        screenshot = self.getUrlFromData("ss")
        titleScreen = self.getUrlFromData("sstitle")

        defCartridge = self.formatPublicUrl({
            "media": "wheel-carbon",
            "maxwidth": 256,
        })
        defScreenshot = self.formatPublicUrl({
            "media": "screenmarquee",
            "maxwidth": "1600",
            "maxheight": "480",
        })
        defTitleScreen = self.formatPublicUrl({
            "media": "background",
            "maxwidth": "1600",
            "maxheight": "480",
        })

        return GameMedia(
            rom=self.__rom,

            cartridgeUrl=cartridge,
            screenshotUrl=screenshot,
            titleScreenUrl=titleScreen,

            defaultCartridgeUrl=defCartridge,
            defaultScreenshotUrl=defScreenshot,
            defaultTitleScreenUrl=defTitleScreen,
        )

    @staticmethod
    def getBestOf(images: list[dict], tag: str, valueList: list[str], fallback=None):
        for value in valueList:
            for image in images:
                if image.get(tag) == value:
                    return image
        return fallback

    def getUrlFromData(self, mediaType: str):
        goodMedias = [x for x in self.__data if x.get("type") == mediaType]
        regionalMedia = self.getBestOf(goodMedias, "region", regions)
        if regionalMedia is None:
            return None
        return furl(regionalMedia.get("url"))

    def formatPublicUrl(self, extraParams: dict):
        url = furl(basePublicUrl)
        baseParams = {
            "plateformid": str(self.__rom.console.id),
            "region": "wor"
        }
        url.set(baseParams)
        url.add(extraParams)
        return url
