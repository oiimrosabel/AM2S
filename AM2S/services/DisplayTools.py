import sys

from AM2S.enums.TerminalColor import TerminalColor as Tc, colorText as cT


class DisplayTools:
    @staticmethod
    def task(text: str):
        print(f"\r{cT("🛈 TASK", Tc.TASK)} {text}")

    @staticmethod
    def info(text: str):
        print(f"\r{cT("🮕 DEBUG", Tc.INFO)} {text}")

    @staticmethod
    def warning(text: str):
        print(f"\r{cT("⚠ WARNING", Tc.WARNING)} {text}", file=sys.stderr)

    @staticmethod
    def error(text: str):
        print(f"\r{cT("⨉ ERROR", Tc.ERROR)} {text}", file=sys.stderr)

    @staticmethod
    def success(text: str):
        print(f"\r{cT("✓ SUCCESS", Tc.SUCCESS)} {text}")

    @staticmethod
    def ask(text: str, choices: list[str], default=0) -> int:
        question = f"\r{cT("🯄 QUESTION", Tc.ASK)} {text} (default = {default}) \n"
        for index, choice in enumerate(choices):
            question += f"\r\t{index} : {choice}\n"
        question += " < "
        res = input(question)
        if res == "":
            DisplayTools.info(f"Chose {choices[default]} ({default}, default).")
            return default
        try:
            res = int(res)
        except ValueError:
            DisplayTools.error("Invalid input. Try again.")
            return DisplayTools.ask(text, choices, default)
        if res < 0 or res > len(choices):
            DisplayTools.error("Invalid input. Try again.")
            return DisplayTools.ask(text, choices, default)
        DisplayTools.info(f"Chose {choices[res]} ({res}).")
        return res
