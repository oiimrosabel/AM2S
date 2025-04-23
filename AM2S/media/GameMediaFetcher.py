from pathlib import Path
from shutil import rmtree
from urllib.request import urlretrieve

from PIL import Image, ImageFilter, ImageEnhance
from furl import furl

from AM2S.errors.ImageError import ImageError
from AM2S.media.GameMedia import GameMedia
from AM2S.media.MaskApplier import MaskApplier
from AM2S.misc.NodeTools import NodeTools as Nt
from AM2S.misc.TomlLoader import TomlLoader


class GameMediaGetter:
    __medias: GameMedia
    __config: TomlLoader
    __masker: MaskApplier

    def __init__(self, media: GameMedia, config: TomlLoader, maskPath: Path):
        self.__medias = media
        self.__config = config
        self.__masker = MaskApplier(maskPath, config)

    def downloadBoxArt(self, path: Path):
        path = Nt.getFolder(path)

        screenDims: list[int] = self.__config.get("images/dimensions/screenDims", [640, 480])
        barsSizes: list[int] = self.__config.get("images/dimensions/barsSizes", [43, 42])
        padding: int = self.__config.get("images/dimensions/padding", 12)
        withCartridge: bool = self.__config.get("images/filters/withCartridge", False)

        resFileName = self.__medias.rom.name + ".png"
        resSavePath = path / resFileName
        background = Image.new("RGBA", screenDims, (255,) * 4)

        tempFolder = Nt.createOrResetFolder(path / "__temp")
        titleScreenPath = tempFolder / "ttl.png"
        titleScreenImage = self.__retrieveTitleScreenImage(titleScreenPath)

        background = self.__resizeToCover(background, titleScreenImage)
        background = self.__applyFilters(background)
        background = self.__masker.apply(background)

        if withCartridge:
            cartridgePath = tempFolder / "crt.png"
            cartridgeImage = self.__retrieveCartridgeImage(cartridgePath)
            background = self.__addCartridgeToImage(
                background,
                cartridgeImage,
                [padding, padding + barsSizes[1]]
            )

        background.save(resSavePath)
        rmtree(tempFolder)

    def downloadScreenshot(self, path: Path):
        path = Nt.getFolder(path)

        savePath = path / (self.__medias.rom.name + ".png")
        try:
            urlretrieve(self.__medias.screenshotUrl.url, savePath)
        except:
            urlretrieve(self.__medias.defaultScreenshotUrl.url, savePath)

    def __applyFilters(self, background: Image) -> Image:
        brightness: float = self.__config.get("images/filters/brightness", 1.)
        blurLevel: int = self.__config.get("images/filters/blurLevel", 0)

        background = ImageEnhance.Brightness(background).enhance(brightness)
        background = background.filter(ImageFilter.GaussianBlur(blurLevel))
        return background

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
        raise ImageError("No title screen image found")

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
    def __resizeToCover(background: Image, image: Image) -> Image:
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
    def __addCartridgeToImage(background: Image, cartridge: Image, padding: list[int]) -> Image:
        ogW, ogH = cartridge.size
        bgW, bgH = background.size

        imageOffset = (bgW - padding[0] - ogW, bgH - padding[1] - ogH)
        background.alpha_composite(cartridge, imageOffset)
        return background
