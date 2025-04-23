from pathlib import Path
from zipfile import ZipFile

from loguru import logger

from AM2S.procedure.Procedure import Procedure


class ZipProcedure(Procedure):
	def apply(self, path: Path) -> Path | None:
		if path.suffix != ".zip":
			return path
		logger.info("ZipProcedure launched")

		with ZipFile(path, "r") as zipFile:
			fileList = zipFile.namelist()
			biggestFile = ""
			biggestFileSize = 0
			for file in fileList:
				info = zipFile.getinfo(file)
				if info.file_size > biggestFileSize:
					biggestFile = file
			zipFile.extract(member=biggestFile, path=path.parent)
		return path.parent / biggestFile

	@staticmethod
	def getBiggestFile(zipFile: ZipFile) -> str:
		fileList = zipFile.namelist()
		biggestFile = ("", 0)
		for file in fileList:
			fileSize = zipFile.getinfo(file).file_size
			if fileSize > biggestFile[1]:
				biggestFile = (file, fileSize)
		return biggestFile[0]
