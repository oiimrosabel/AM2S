from os import makedirs
from pathlib import Path
from shutil import rmtree

from AM2S.errors.NodeError import NodeError


class NodeTools:
    @staticmethod
    def createOrResetFolder(path: Path) -> Path:
        if path.is_file():
            raise NodeError(f"{path} is a file")
        if path.exists():
            rmtree(path)
        makedirs(path)
        return path

    @staticmethod
    def getOrCreateFolder(path: Path) -> Path:
        if not path.exists():
            makedirs(path)
            return path
        if path.is_file():
            raise NodeError(f"{path} is not a folder")
        return path

    @staticmethod
    def getFolder(path: Path) -> Path:
        if not path.exists():
            raise NodeError(f"{path} doesn't exist")
        if path.is_file():
            raise NodeError(f"{path} is not a folder")
        return path

    @staticmethod
    def getFile(path: Path) -> Path:
        if not path.exists():
            raise NodeError(f"{path} doesn't exist")
        if path.is_dir():
            raise NodeError(f"{path} is not a file")
        return path
