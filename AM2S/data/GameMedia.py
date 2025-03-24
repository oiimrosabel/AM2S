from dataclasses import dataclass

from furl import furl

from AM2S.data.RomFile import RomFile


@dataclass
class GameMedia:
    rom: RomFile

    cartridgeUrl: furl
    screenshotUrl: furl
    titleScreenUrl: furl

    defaultCartridgeUrl: furl
    defaultScreenshotUrl: furl
    defaultTitleScreenUrl: furl
