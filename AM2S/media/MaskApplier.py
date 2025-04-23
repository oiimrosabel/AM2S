from pathlib import Path

from PIL import Image
from PIL.ImageDraw import ImageDraw

from AM2S.misc.TomlLoader import TomlLoader


class MaskApplier:
	__maskPath: Path
	__config: TomlLoader

	def __init__(self, maskPath: Path, config: TomlLoader):
		self.__maskPath = maskPath
		self.__config = config

	def apply(self, background: Image) -> Image:
		maskName = self.__config.get("images/filters/mask")
		if maskName is None:
			return background
		elif maskName == "Bars":
			return self.__applyBarsMask(background)
		else:
			maskImage = self.__retrieveMask(maskName)
			return self.__applyMask(background, maskImage)

	def __retrieveMask(self, maskName: str) -> Image:
		maskPath = self.__maskPath / f"{maskName}.png"
		try:
			maskImage = Image.open(maskPath)
			return maskImage
		except FileNotFoundError:
			return None

	@staticmethod
	def __applyMask(background: Image, mask: Image):
		newBackground = Image.new("RGBA", background.size, (0,) * 4)
		newBackground.paste(background, mask=mask)
		return newBackground

	def __applyBarsMask(self, background: Image) -> Image:
		bgW, bgH = background.size
		headers = ImageDraw(background, "RGBA")
		fillColor = (0, 0, 0, 0)

		barSizes: list[int] = self.__config.get(
			"images/dimensions/barsSizes", [42, 42]
		)
		headers.rectangle([0, 0, bgW, barSizes[0]], fill=fillColor)
		headers.rectangle([0, bgH - barSizes[1], bgW, bgH], fill=fillColor)

		return background
