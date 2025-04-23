from enum import StrEnum


class HashAlgorithm(StrEnum):
	CRC32 = "crc32"
	SHA1 = "sha1sum"
	MD5 = "md5sum"
