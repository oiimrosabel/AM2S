from argparse import ArgumentParser
from pathlib import Path

import dpath


class ArgumentService:
    __parser: ArgumentParser
    __result: dict
    __folders: list[Path]

    def __init__(self):
        parser = ArgumentParser(
            prog="AM2S",
            description="Another MuOS Simple Scraper"
        )

        parser.add_argument(
            "folder",
            nargs="+",
            help="the paths of the folders to scan",
            type=lambda p: Path(p)
        )
        parser.add_argument(
            "-b", "--noBoxArt",
            action="store_true",
            default=False,
            help="do not download the \"box art\" image"
        )
        parser.add_argument(
            "-s", "--noScreenshots",
            action="store_true",
            default=False,
            help="do not download the \"screenshots\" image"
        )
        parser.add_argument(
            "-t", "--noText",
            action="store_true",
            default=False,
            help="do not download the game description"
        )
        parser.add_argument(
            "-f", "--failFast",
            action="store_true",
            default=False,
            help="exits immediately if an error occurs"
        )

        self.__parser = parser

    def parse(self):
        self.__result = vars(self.__parser.parse_args())

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item, default=None):
        return dpath.get(
            self.__result,
            item,
            default=default
        )
