import subprocess
from enum import StrEnum
from pathlib import Path

from AM2S.types.Record import Record


class HashAlgorithm(StrEnum):
    CRC32 = "crc32"
    SHA1 = "sha1sum"
    MD5 = "md5sum"


class Hasher(Record):
    crc32 = str
    sha1 = str
    md5 = str

    @staticmethod
    def callAlgorithm(algo: HashAlgorithm, path: Path) -> str:
        res = subprocess.check_output([algo, str(path)], encoding="utf-8")
        return res.split(" ")[0].strip().upper()

    def __init__(self, path: Path):
        self.crc32 = self.callAlgorithm(HashAlgorithm.CRC32, path)
        self.sha1 = self.callAlgorithm(HashAlgorithm.SHA1, path)
        self.md5 = self.callAlgorithm(HashAlgorithm.MD5, path)
