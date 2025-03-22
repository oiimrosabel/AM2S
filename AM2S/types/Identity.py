from AM2S.types.Logins import Logins
from AM2S.types.Record import Record


class Identity(Record):
    dev: Logins
    account: Logins

    def __init__(self, devlog: str, devpwd: str, login: str, pwd: str):
        self.dev = Logins(devlog, devpwd)
        self.account = Logins(login, pwd)
