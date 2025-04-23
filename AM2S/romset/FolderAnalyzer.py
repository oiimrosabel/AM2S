from pathlib import Path

from AM2S.console.ConsoleDatabase import ConsoleDatabase
from AM2S.display.DisplayTools import DisplayTools as Dt
from AM2S.errors.RomError import RomError
from AM2S.misc.NodeTools import NodeTools as Nt
from AM2S.misc.TomlLoader import TomlLoader
from AM2S.rom.RomFileBuilder import RomFileBuilder
from AM2S.romset.RomSet import RomSet


class FolderAnalyzer:
	__db: ConsoleDatabase
	__nonFormats: list[str]
	__hintName: str

	def __init__(
		self, database: ConsoleDatabase, hintName=".hint", nonFormats=None
	):
		if nonFormats is None:
			nonFormats = []
		self.__db = database
		self.__hintName = hintName
		self.__nonFormats = nonFormats

	def __getHint(self, path: Path, suffix: str):
		try:
			hintPath = Nt.getFile(path / self.__hintName)
		except Exception as e:
			Dt.error(f"An error occured : {e}")
			return None
		if suffix[0] == ".":
			suffix = suffix[1:]
		hint = TomlLoader(hintPath).get(suffix)

		Dt.info(f'Found hint "{hint}" for {suffix}')
		return hint

	def __getConsoleFromFormat(self, suffix: str, rootPath: Path):
		res = self.__db.searchByFormat(suffix)
		match len(res):
			case 0:
				raise RomError(f"{suffix} is not a valid format")
			case 1:
				return res[0]
			case _:
				if (hint := self.__getHint(rootPath, suffix)) is None:
					raise RomError(f"{suffix} is ambiguous. Please add a hint")
				resHint = self.__db.searchByHint(hint)
				if len(resHint) != 1:
					raise RomError(
						f"{suffix} is ambiguous. Please check your hint"
					)
				return resHint[0]

	@staticmethod
	def __createDataFolder(rootPath: Path, dataFolderName: str):
		rootPath = Nt.getFolder(rootPath)
		dataPath = Nt.createOrResetFolder(rootPath / dataFolderName)
		boxPath = Nt.getOrCreateFolder(dataPath / "box")
		previewPath = Nt.getOrCreateFolder(dataPath / "preview")
		textPath = Nt.getOrCreateFolder(dataPath / "text")
		return boxPath, previewPath, textPath

	def scan(self, path: Path) -> list[RomSet]:
		path = Nt.getFolder(path)
		formatToRomset: dict[str, RomSet] = {}

		for node in path.rglob("*.*"):
			if node.is_dir() or (romFormat := node.suffix) in self.__nonFormats:
				continue

			if romFormat not in formatToRomset.keys():
				try:
					console = self.__getConsoleFromFormat(romFormat, path)
				except Exception as e:
					Dt.error(f"An error occured : {e}")
					continue
				(boxPath, previewPath, textPath) = self.__createDataFolder(
					path, console.genericName
				)
				newRomSet = RomSet(
					console=console,
					root=path,
					textPath=textPath,
					previewPath=previewPath,
					boxPath=boxPath,
					games=[],
				)
				formatToRomset[romFormat] = newRomSet

			romSet = formatToRomset.get(romFormat)
			rom = RomFileBuilder(node, romSet.console).build()
			romSet.games.append(rom)

		return list(formatToRomset.values())
