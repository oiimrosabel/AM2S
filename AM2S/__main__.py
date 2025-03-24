from os import makedirs
from pathlib import Path

from AM2S.builders.IdentityBuilder import IdentityBuilder
from AM2S.builders.RomFileBuilder import RomFileBuilder
from AM2S.services.ArgumentsService import ArgumentService
from AM2S.services.ConfigLoader import ConfigLoader
from AM2S.services.DisplayTools import DisplayTools as Dt
from AM2S.services.GameInfoFormatter import GameInfoFormatter
from AM2S.services.GameMediaFetcher import GameMediaGetter
from AM2S.services.InfoRequester import InfoRequester


def main():
    configPath = Path(__file__).parent.parent / "config.toml"
    config = ConfigLoader(configPath)
    identity = IdentityBuilder(config).build()

    getter = InfoRequester(identity)
    args = ArgumentService()
    args.parse()

    roots = args.get("folder", [])

    for root in roots:
        if not root.exists():
            Dt.error(f"The folder '{root}' does not exist.")
            exit(1)
        if not root.is_dir():
            Dt.error(f"{root} is not a folder.")
            exit(1)

        filesToAnalyze = [x for x in root.rglob("*.[!txt][!png]*")]
        noBoxArt = args.get("noBoxArt", False)
        noScreenshots = args.get("noScreenshots", False)
        noText = args.get("noText", False)

        print("")
        Dt.info(f"Folder to analyze: {root.name}")
        Dt.info(f"Number of games to scrape : {len(filesToAnalyze)}")
        if noBoxArt:
            Dt.info("The \"box art\" images won't be downloaded.")
        if noScreenshots:
            Dt.info("The screenshots won't be downloaded.")
        if noText:
            Dt.info("The game descriptions won't be downloaded.")
        print("")

        for file in filesToAnalyze:
            try:
                Dt.task(f"Scraping {file.name}, this might take a while...")
                rom = RomFileBuilder(file).build()
                dataFolder = root / rom.console.genericName
                if not dataFolder.exists():
                    makedirs(dataFolder)
                info = getter.getData(rom)
                textFormatter = GameInfoFormatter(info)
                imageGetter = GameMediaGetter(dataFolder, info.medias, config)
                if not noBoxArt:
                    imageGetter.downloadBoxArt()
                if not noScreenshots:
                    imageGetter.downloadScreenshot()
                if not noText:
                    textFormatter.saveResult(dataFolder / "text")
                Dt.success(f"{file.name} has been successfully scraped.")
            except Exception as e:
                if args.get("failFast", False):
                    Dt.error(f"{e}.")
                    raise e
                else:
                    Dt.error(f'{e}. Skipping {file.stem}...')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Dt.success("Ctrl-C caught. Exiting...")
