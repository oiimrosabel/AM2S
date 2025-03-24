from os import makedirs
from pathlib import Path
from shutil import rmtree
from urllib.request import urlretrieve

from PIL import Image, ImageFilter, ImageEnhance
from PIL.ImageDraw import ImageDraw
from furl import furl

from AM2S.data.GameMedia import GameMedia
from AM2S.services.ConfigLoader import ConfigLoader


class GameMediaGetter:
    __savePath: Path
    __medias: GameMedia
    __config: ConfigLoader

    def __init__(self, save: Path, media: GameMedia, config: ConfigLoader):
        if not save.exists() or save.is_file():
            raise Exception(f"{save} does not exist")

        self.__savePath = save
        self.__medias = media
        self.__config = config

    def downloadBoxArt(self):
        boxArtFolder = self.__savePath / "box"
        if not boxArtFolder.exists():
            makedirs(boxArtFolder)

        screenDims: list[int] = self.__config.get("images/screenDims", [640, 480])
        barsSizes: list[int] = self.__config.get("images/barsSizes", [43, 42])
        noBars: bool = self.__config.get("images/noBars", False)
        padding: int = self.__config.get("images/padding", 12)

        resFileName = self.__medias.rom.path.stem + ".png"
        resSavePath = boxArtFolder / resFileName

        tempFolder = boxArtFolder / "__temp"
        if tempFolder.exists():
            rmtree(tempFolder)
        makedirs(tempFolder)

        background = Image.new("RGBA", screenDims, (255,) * 4)
        titleScreenPath = tempFolder / "1.png"
        cartridgePath = tempFolder / "2.png"

        titleScreenImage = self.__retrieveTitleScreenImage(titleScreenPath)
        cartridgeImage = self.__retrieveCartridgeImage(cartridgePath)

        background = self.__resizeToCover(background, titleScreenImage)
        background = background.filter(ImageFilter.GaussianBlur(16))
        background = ImageEnhance.Brightness(background).enhance(0.7)
        background = self.__addCartridgeToImage(background, cartridgeImage, [padding, padding + barsSizes[1]])
        if not noBars:
            background = self.__addHeaderAndFooter(background, barsSizes)

        background.save(resSavePath)
        rmtree(tempFolder)

    def downloadScreenshot(self):
        screenshotFolder = self.__savePath / "preview"
        if not screenshotFolder.exists():
            makedirs(screenshotFolder)

        savePath = screenshotFolder / (self.__medias.rom.path.stem + ".png")
        try:
            urlretrieve(self.__medias.screenshotUrl.url, savePath)
        except:
            urlretrieve(self.__medias.defaultScreenshotUrl.url, savePath)

    def __retrieveTitleScreenImage(self, path: Path) -> Image:
        candidates: list[furl] = [
            self.__medias.titleScreenUrl,
            self.__medias.screenshotUrl,
            self.__medias.defaultTitleScreenUrl
        ]

        for candidate in candidates:
            if candidate is not None:
                urlretrieve(candidate.url, path)
                image = Image.open(path, mode="r")
                return image
        raise Exception("No title screen image found")

    def __retrieveCartridgeImage(self, path: Path) -> Image:
        try:
            urlretrieve(self.__medias.cartridgeUrl.url, path)
            cartridgeImage = Image.open(path, mode="r")
            cartridgeImage = self.__resizeToWidth(cartridgeImage, self.__medias.rom.console.preferredWidth)
        except:
            urlretrieve(self.__medias.defaultCartridgeUrl.url, path)
            cartridgeImage = Image.open(path, mode="r")
        return cartridgeImage

    @staticmethod
    def __resizeToWidth(image: Image, width: int) -> Image:
        imW, imH = image.size
        newHeight = int(width * (imH / imW))
        return image.resize((width, newHeight))

    @staticmethod
    def __resizeToCover(background: Image, image: Image):
        ogW, ogH = image.size
        bgW, bgH = background.size

        imageRatio = ogW / ogH
        bgRatio = bgW / bgH

        if bgRatio > imageRatio:
            newDim = (bgW, int(bgW // imageRatio))
        else:
            newDim = (int(bgH * imageRatio), bgH)

        image = image.resize(newDim)
        imageOffset = ((bgW - newDim[0]) // 2, (bgH - newDim[1]) // 2)
        background.paste(image, imageOffset)
        return background

    @staticmethod
    def __addCartridgeToImage(background: Image, cartridge: Image, padding: list[int]):
        ogW, ogH = cartridge.size
        bgW, bgH = background.size

        imageOffset = (bgW - padding[0] - ogW, bgH - padding[1] - ogH)
        background.alpha_composite(cartridge, imageOffset)
        return background

    @staticmethod
    def __addHeaderAndFooter(background: Image, barSizes: list[int]):
        bgW, bgH = background.size
        headers = Image.new("RGBA", background.size, (0,) * 4)
        fillColor = (0, 0, 0, 96)

        canvas = ImageDraw(headers)
        canvas.rectangle([0, 0, bgW, barSizes[0]], fill=fillColor)
        canvas.rectangle([0, bgH - barSizes[1], bgW, bgH], fill=fillColor)
        background.alpha_composite(headers, (0,) * 2)
        return background
