import subprocess
from pathlib import Path

from AM2S.data.Hashes import Hashes
from AM2S.enums.HashAlgorithm import HashAlgorithm
from AM2S.interfaces.Builder import Builder


class HashesBuilder(Builder[Hashes]):
    __path: Path

    def __init__(self, path: Path):
        self.__path = path

    def build(self) -> Hashes:
        return Hashes(
            crc32=self.callAlgorithm(HashAlgorithm.CRC32),
            sha1=self.callAlgorithm(HashAlgorithm.SHA1),
            md5=self.callAlgorithm(HashAlgorithm.MD5),
        )

    def callAlgorithm(self, algo: HashAlgorithm) -> str:
        res = subprocess.check_output([algo, str(self.__path)], encoding="utf-8")
        return res.split(" ")[0].strip()
