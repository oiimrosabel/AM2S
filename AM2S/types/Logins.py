from AM2S.types.Record import Record


class Logins(Record):
    login: str
    password: str

    def __init__(self, login: str, pwd: str):
        self.login = login
        self.password = pwd
