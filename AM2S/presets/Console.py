from AM2S.presets.BoxSizes import BoxSizes
from AM2S.types.Console import Console

Doom = Console(135, ".wad", BoxSizes.MID)
GameBoy = Console(9, ".gb", BoxSizes.MID)
GameBoyAdvance = Console(12, ".gba", BoxSizes.WIDE)
GameBoyColor = Console(10, ".gbc", BoxSizes.MID)
Famicom = Console(3, ".nes", BoxSizes.MID)
SuperFamicom = Console(4, ".sfc", BoxSizes.WIDE)
Pico8 = Console(234, ".p8", BoxSizes.MID)
Sega32x = Console(19, ".32x", BoxSizes.WIDE)
MasterSystem = Console(2, ".sms", BoxSizes.WIDE)
MegaCD = Console(20, ".chd", BoxSizes.MID)
MegaDrive = Console(1, ".md", BoxSizes.WIDE)
Windows = Console(138, ".sh", BoxSizes.MID)

consoleList = [Doom,
               GameBoy, GameBoyAdvance, GameBoyColor,
               Famicom, SuperFamicom,
               Pico8,
               Sega32x, MasterSystem, MegaCD, MegaDrive,
               Windows]

suffixToConsole = {c.suffix: c for c in consoleList}
