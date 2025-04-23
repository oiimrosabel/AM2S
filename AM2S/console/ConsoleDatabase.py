from pathlib import Path

from AM2S.console.ConsoleInfo import ConsoleInfo
from AM2S.console.ConsoleInfoBuilder import ConsoleInfoBuilder
from AM2S.errors.DatabaseError import DatabaseError
from AM2S.misc.TomlLoader import TomlLoader


class ConsoleDatabase:
	__db: list[dict]

	def __init__(self, path: Path):
		self.path = path
		loader = TomlLoader(path)
		if (db := loader.get("console")) is None:
			raise DatabaseError(f"Malformed console database : {path}")
		self.__db = db

	def searchByFormat(self, fileFormat: str) -> list[ConsoleInfo]:
		res = []
		for entry in self.__db:
			if fileFormat in entry.get("format", []):
				res.append(ConsoleInfoBuilder(entry).build())
		return res

	def searchByHint(self, hint: str) -> list[ConsoleInfo]:
		for entry in self.__db:
			if (entry.get("hint", "")) == hint:
				return [ConsoleInfoBuilder(entry).build()]
		return []
