from pathlib import Path

from AM2S.console.ConsoleInfo import ConsoleInfo
from AM2S.errors.RomError import RomError
from AM2S.hash.HashesBuilder import HashesBuilder
from AM2S.misc.NodeTools import NodeTools as Nt
from AM2S.rom.RomFile import RomFile
from AM2S.templates.Builder import Builder


class RomFileBuilder(Builder[RomFile]):
	__path: Path
	__console: ConsoleInfo

	def __init__(self, path: Path, console: ConsoleInfo):
		self.__path = path
		self.__console = console

	def build(self) -> RomFile:
		oldPath = Nt.getFile(self.__path)

		procedure = self.__console.procedure
		newPath = procedure.apply(oldPath)
		if newPath is None:
			raise RomError(f"The file got rejected: {oldPath}")
		newPath = Nt.getFile(newPath)

		return RomFile(
			name=oldPath.stem,
			path=newPath,
			hash=HashesBuilder(newPath).build(),
			console=self.__console,
			size=newPath.stat().st_size,
		)
