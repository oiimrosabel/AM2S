from dataclasses import dataclass
from pathlib import Path

from AM2S.console.ConsoleInfo import ConsoleInfo
from AM2S.hash.Hashes import Hashes


@dataclass
class RomFile:
	name: str
	path: Path
	hash: Hashes
	console: ConsoleInfo
	size: int
