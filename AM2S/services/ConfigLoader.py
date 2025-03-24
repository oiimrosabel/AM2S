from pathlib import Path
from tomllib import load

import dpath


class ConfigLoader:
    __config: dict

    def __init__(self, path: Path):
        with open(path, 'rb') as f:
            self.__config = load(f)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item, default=None):
        return dpath.get(
            self.__config,
            item,
            default=default
        )
