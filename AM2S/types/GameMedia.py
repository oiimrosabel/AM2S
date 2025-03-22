from AM2S.types.Record import Record
from AM2S.types.RomFile import RomFile

regions = ["eu", "us", "wor", "jp", "ss"]


class GameMedia(Record):
    cartridgeUrl: str
    screenshotUrl: str
    titleScreenUrl: str
    of: RomFile

    def __init__(self, data: list[dict], of: RomFile):
        self.of = of
        self.cartridgeUrl = self.getUrlFromData(data, "support-2D")
        self.screenshotUrl = self.getUrlFromData(data, "ss")
        self.titleScreenUrl = self.getUrlFromData(data, "sstitle")

    @staticmethod
    def filterListByTag(data: list[dict], tag: str, value: str):
        return [x for x in data if x.get(tag) == value]

    @staticmethod
    def getBestOf(images: list[dict], tag: str, valueList: list[str], fallback=None):
        for value in valueList:
            for image in images:
                if image.get(tag) == value:
                    return image
        return fallback

    def getUrlFromData(self, data: list[dict], mediaType: str):
        goodMedias = self.filterListByTag(data, "type", mediaType)
        regionalMedia = self.getBestOf(goodMedias, "region", regions)
        if regionalMedia is None:
            return None
        return regionalMedia.get("url")
