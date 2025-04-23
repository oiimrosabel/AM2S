from dataclasses import dataclass

from AM2S.media import GameMedia
from AM2S.rom.RomFile import RomFile


@dataclass
class GameInfo:
	rom: RomFile
	releaseDate: str
	nbOfPlayers: str
	editor: str
	synopsis: str
	genres: list[str]
	medias: GameMedia
