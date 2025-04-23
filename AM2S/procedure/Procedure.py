from abc import abstractmethod
from pathlib import Path


class Procedure:
	@abstractmethod
	def apply(self, path: Path) -> Path | None:
		pass
