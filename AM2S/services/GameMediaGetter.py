from os import makedirs
from pathlib import Path
from shutil import rmtree
from urllib.request import urlretrieve

from PIL import Image, ImageFilter, ImageEnhance
from PIL.ImageDraw import ImageDraw

from AM2S.types.GameMedia import GameMedia


class GameMediaGetter:
    savePath: Path

    screenshotFolder: Path
    boxArtFolder: Path

    medias: GameMedia

    def __init__(self, save: Path, media: GameMedia):
        if not save.exists():
            makedirs(save)

        screenshotFolder = save / "preview"
        if not screenshotFolder.exists():
            makedirs(screenshotFolder)

        boxArtFolder = save / "box"
        if not boxArtFolder.exists():
            makedirs(boxArtFolder)

        self.screenshotFolder = screenshotFolder
        self.boxArtFolder = boxArtFolder

        self.savePath = save
        self.medias = media

    def downloadBoxArt(self, canvasSize=(640, 480), barSizes=(43, 42), padding=12):
        resFileName = self.medias.of.path.stem + ".png"
        resSavePath = self.boxArtFolder / resFileName

        tempFolder = self.boxArtFolder / "__temp"
        if tempFolder.exists():
            rmtree(tempFolder)
        makedirs(tempFolder)

        background = Image.new("RGBA", canvasSize, (255,) * 4)

        titleScreenPath = tempFolder / "1.png"
        cartridgePath = tempFolder / "2.png"

        titleScreenImage = self.retrieveTitleScreenImage(titleScreenPath)
        cartridgeImage = self.retrieveCartridgeImage(cartridgePath)

        background = self.resizeToCover(background, titleScreenImage)
        background = background.filter(ImageFilter.GaussianBlur(16))
        background = ImageEnhance.Brightness(background).enhance(0.7)
        background = self.addCartridgeToImage(background, cartridgeImage, (padding, padding + barSizes[1]))
        background = self.addHeaderAndFooter(background, barSizes)
        background.save(resSavePath)
        rmtree(tempFolder)

    def retrieveTitleScreenImage(self, path: Path) -> Image:
        candidates = [
            self.medias.titleScreenUrl,
            self.medias.screenshotUrl,
            self.medias.of.console.getDefaultTitleScreenUrl()
        ]

        for candidate in candidates:
            if candidate is not None:
                urlretrieve(candidate, path)
                image = Image.open(path, mode="r")
                return image
        raise Exception("No title screen image found")

    def retrieveCartridgeImage(self, path: Path) -> Image:
        try:
            urlretrieve(self.medias.cartridgeUrl, path)
            cartridgeImage = Image.open(path, mode="r")
            cartridgeImage = self.resizeToWidth(cartridgeImage, self.medias.of.console.width)
        except:
            urlretrieve(self.medias.of.console.getDefaultCartridgeUrl(), path)
            cartridgeImage = Image.open(path, mode="r")
        return cartridgeImage

    @staticmethod
    def resizeToWidth(image: Image, width: int) -> Image:
        imW, imH = image.size
        newHeight = int(width * (imH / imW))
        return image.resize((width, newHeight))

    @staticmethod
    def resizeToCover(background: Image, image: Image):
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
    def addCartridgeToImage(background: Image, cartridge: Image, padding: tuple[int, int]):
        ogW, ogH = cartridge.size
        bgW, bgH = background.size

        imageOffset = (bgW - padding[0] - ogW, bgH - padding[1] - ogH)
        background.alpha_composite(cartridge, imageOffset)
        return background

    @staticmethod
    def addHeaderAndFooter(background: Image, barSizes: tuple[int, int]):
        bgW, bgH = background.size
        headers = Image.new("RGBA", background.size, (0,) * 4)

        fillColor = (0, 0, 0, 96)

        canvas = ImageDraw(headers)
        canvas.rectangle([0, 0, bgW, barSizes[0]], fill=fillColor)
        canvas.rectangle([0, bgH - barSizes[1], bgW, bgH], fill=fillColor)

        background.alpha_composite(headers, (0,) * 2)
        return background

    def downloadScreenshot(self):
        savePath = self.screenshotFolder / (self.medias.of.path.stem + ".png")
        try:
            urlretrieve(self.medias.screenshotUrl, savePath)
        except:
            urlretrieve(self.medias.of.console.getDefaultScreenshotUrl(), savePath)
