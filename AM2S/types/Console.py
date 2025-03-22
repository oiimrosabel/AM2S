from urllib.parse import urlunsplit, urlencode

from AM2S.presets.BoxSizes import BoxSizes
from AM2S.types.Record import Record

basePublicUrl = urlunsplit(("https", "www.screenscraper.fr", "image.php", "", ""))


class Console(Record):
    id: int
    suffix: str
    width: int

    def __init__(self, consoleId: int, suffix: str, width=BoxSizes.WIDE):
        self.id = consoleId
        self.suffix = suffix
        self.width = width

    def formatPublicUrl(self, extraParams: dict):
        params = {
            "plateformid": str(self.id),
            "region": "wor"
        }
        params.update(extraParams)
        return f"{basePublicUrl}?{urlencode(params)}"

    def getDefaultScreenshotUrl(self):
        extraParams = {
            "media": "screenmarquee",
            "maxwidth": "1600",
            "maxheight": "480",
        }
        return self.formatPublicUrl(extraParams)

    def getDefaultTitleScreenUrl(self):
        extraParams = {
            "media": "background",
            "maxwidth": "1600",
            "maxheight": "480",
        }
        return self.formatPublicUrl(extraParams)

    def getDefaultCartridgeUrl(self):
        extraParams = {
            "media": "wheel-carbon",
            "maxwidth": str(BoxSizes.WIDE),
        }
        return self.formatPublicUrl(extraParams)
