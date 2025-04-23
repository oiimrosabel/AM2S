from dataclasses import dataclass


@dataclass
class Hashes:
	crc32: str
	sha1: str
	md5: str
