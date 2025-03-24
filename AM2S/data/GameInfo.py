from dataclasses import dataclass

from AM2S.data import GameMedia
from AM2S.data.RomFile import RomFile


@dataclass
class GameInfo:
    rom: RomFile
    releaseDate: str
    nbOfPlayers: str
    editor: str
    synopsis: str
    genres: list[str]
    medias: GameMedia
