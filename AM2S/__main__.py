import time
from pathlib import Path

from alive_progress import alive_bar

from AM2S.api.InfoRequester import InfoRequester
from AM2S.console.ConsoleDatabase import ConsoleDatabase
from AM2S.display.DisplayTools import DisplayTools as Dt
from AM2S.display.TerminalColor import colorText as cT, TerminalColor as Tc
from AM2S.info.GameInfoFormatter import GameInfoFormatter
from AM2S.media.GameMediaFetcher import GameMediaGetter
from AM2S.misc.ArgumentsService import ArgumentService
from AM2S.misc.NodeTools import NodeTools as Nt
from AM2S.misc.TomlLoader import TomlLoader
from AM2S.romset.FolderAnalyzer import FolderAnalyzer

args = ArgumentService()
args.parse()


def main():
	root = Path(__file__).parent.parent

	configPath = root / "config.toml"
	maskPath = root / "masks"
	config = TomlLoader(configPath)
	getter = InfoRequester(config)

	dbPath = root / "consoles.toml"
	consoleDb = ConsoleDatabase(dbPath)

	scannedFolders = args.get("folder", [])

	startTime = time.time()

	for folder in scannedFolders:
		try:
			folder = Nt.getFolder(folder)
		except Exception as e:
			Dt.error(str(e))
			exit(1)

		romsets = FolderAnalyzer(
			consoleDb,
			config.get("scan/hintFile", ""),
			config.get("scan/ignoredFormat", []),
		).scan(folder)

		noBoxArt = args.get("noBoxArt", False)
		noScreenshots = args.get("noScreenshots", False)
		noText = args.get("noText", False)

		isLenient = args.get("lenient", False)
		errors = []

		for romset in romsets:
			print("")
			Dt.info(f"Console: {romset.console.genericName}")
			Dt.info(f"Folder to analyze: {romset.root}")
			Dt.info(f"Number of games to scrape : {len(romset.games)}")
			if noBoxArt:
				Dt.info('The "box art" images won\'t be downloaded.')
			if noScreenshots:
				Dt.info("The screenshots won't be downloaded.")
			if noText:
				Dt.info("The game descriptions won't be downloaded.")
			if isLenient:
				Dt.info("Any errors will be ignored.")
			print("")

			for rom in romset.games:
				try:
					taskPrefix = cT("🛈 TASK", Tc.TASK)
					successPrefix = cT("✓ SUCCESS", Tc.SUCCESS)
					with alive_bar(
						6,
						title=f"{taskPrefix} {rom.name} - Scrapping",
						bar="bubbles",
						spinner="twirls",
						title_length=96,
						stats=False,
					) as progress:
						info = getter.getData(rom)
						progress()

						progress.title(
							f"{taskPrefix} {rom.name} - Formatting description"
						)
						textFormatter = GameInfoFormatter(info)
						progress()

						progress.title(
							f"{taskPrefix} {rom.name} - Getting medias"
						)
						imageGetter = GameMediaGetter(
							info.medias, config, maskPath
						)
						progress()

						progress.title(
							f"{taskPrefix} {rom.name} - Generating box art"
						)
						if not noBoxArt:
							boxArtFolder = Nt.getFolder(romset.boxPath)
							imageGetter.downloadBoxArt(boxArtFolder)
						progress()

						progress.title(
							f"{taskPrefix} {rom.name} - Saving screenshot"
						)
						if not noScreenshots:
							screenshotsFolder = Nt.getFolder(romset.previewPath)
							imageGetter.downloadScreenshot(screenshotsFolder)
						progress()

						progress.title(
							f"{taskPrefix} {rom.name} - Saving description"
						)
						if not noText:
							textFolder = Nt.getFolder(romset.textPath)
							textFormatter.saveText(textFolder)
						progress()

						progress.title(f"{successPrefix} {rom.name}")
				except Exception as e:
					if isLenient:
						Dt.warning(f"{e}. Skipping...")
						errors.append(rom.name)
					else:
						Dt.error(f"{e}. Exiting...")
						exit(1)

			errorCount = len(errors)
			Dt.success(
				f"{len(romset.games) - errorCount} ROM(s) for {romset.console.genericName} has been scrapped !"
			)
			if isLenient and errorCount > 0:
				Dt.warning(
					f"{errorCount} error(s) occurred. The following ROMs have not been scrapped:"
				)
				for file in errors:
					print(f"\t- {file}")

	endTime = time.time()
	print("")
	Dt.success(
		f"All done ! It took a total of {round(endTime - startTime, 2)} seconds. Enjoy <3"
	)


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		Dt.success("Ctrl-C caught. Exiting...")
