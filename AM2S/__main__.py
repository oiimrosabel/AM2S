import json
import sys
from pathlib import Path

from AM2S.services.GameInfoFormatter import GameInfoFormatter
from AM2S.services.GameMediaGetter import GameMediaGetter
from AM2S.services.ScreenscraperInfo import ScreenscraperInfo
from AM2S.types.Identity import Identity
from AM2S.types.RomFile import RomFile

if len(sys.argv) < 2:
    print("Usage: python -m AM2S <rom-folder>")
    exit(1)

with open(Path(__file__).parent.parent / "__identity.json") as f:
    data = f.read()
    obj: dict[str, any] = json.loads(data)
    identity = Identity(
        obj.get("devLogin"),
        obj.get("devPassword"),
        obj.get("login"),
        obj.get("password")
    )
    f.close()

getter = ScreenscraperInfo(identity)

roots = []
noBoxArt = False
noScreenshots = False
noText = False

for args in sys.argv[1:]:
    if args == "--noBoxArt":
        print("No box art.")
        noBoxArt = True
    elif args == "--noScreenshots":
        print("No screenshots.")
        noScreenshots = True
    elif args == "--noText":
        print("No text.")
        noText = True
    else:
        roots.append(Path(args))

for root in roots:
    if not (root.exists() and root.is_dir()):
        print(f"Not a folder : {root}")
        exit(1)

    filesToAnalyze = []

    for file in root.rglob("*.*"):
        filesToAnalyze.append(file)

    print(f"Number of games to scrape : {len(filesToAnalyze)}")

    for file in filesToAnalyze:
        try:
            print(f"Scraping {file.name}, this might take a while...")
            rom = RomFile(file)
            dataFolder = root / "data"
            info = getter.getRomInfo(rom)
            textFormatter = GameInfoFormatter(info)
            imageGetter = GameMediaGetter(dataFolder, info.medias)
            if not noBoxArt:
                imageGetter.downloadBoxArt()
            if not noScreenshots:
                imageGetter.downloadScreenshot()
            if not noText:
                textFormatter.saveResult(dataFolder / "text")
        except Exception as e:
            # raise e
            print(f'An exception occurred {e}. Skipping {file.stem}...')
