from dataclasses import dataclass

from AM2S.identity.Credentials import Credentials


@dataclass
class Identity:
    dev: Credentials
    account: Credentials
