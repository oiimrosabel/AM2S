from dataclasses import dataclass

from AM2S.data.Credentials import Credentials


@dataclass
class Identity:
    dev: Credentials
    account: Credentials
