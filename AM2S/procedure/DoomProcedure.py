from pathlib import Path

from loguru import logger

from AM2S.procedure.Procedure import Procedure
from AM2S.procedure.doom.DoomFileDataBuilder import DoomFileDataBuilder


class DoomProcedure(Procedure):
	def apply(self, path: Path):
		if path.suffix != ".doom":
			return path
		logger.info("DoomProcedure launched")
		doomData = DoomFileDataBuilder(path).build()
		if doomData.lastWad is None:
			res = doomData.parentWad
		else:
			res = doomData.lastWad
		logger.info(f"{path.name} references {res}")
		return res
