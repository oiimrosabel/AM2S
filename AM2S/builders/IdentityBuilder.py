from AM2S.data.Credentials import Credentials
from AM2S.data.Identity import Identity
from AM2S.interfaces.Builder import Builder
from AM2S.services.ConfigLoader import ConfigLoader


class IdentityBuilder(Builder[Identity]):
    __config: ConfigLoader

    def __init__(self, config: ConfigLoader):
        self.__config = config

    def build(self) -> Identity:
        return Identity(
            Credentials(
                str(self.__config.get("login/dev/id")),
                str(self.__config.get("login/dev/password")),
            ),
            Credentials(
                str(self.__config.get("login/account/id")),
                str(self.__config.get("login/account/password")),
            )
        )
