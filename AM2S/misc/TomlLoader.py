import tomllib
from pathlib import Path

import dpath

from AM2S.misc.NodeTools import NodeTools as Nt


class TomlLoader:
	__config: dict

	def __init__(self, path: Path):
		path = Nt.getFile(path)
		with open(path, "rb") as f:
			self.__config = tomllib.load(f)

	def __getitem__(self, item):
		return self.get(item)

	def get(self, item: str, default=None):
		return dpath.get(self.__config, item, default=default)
