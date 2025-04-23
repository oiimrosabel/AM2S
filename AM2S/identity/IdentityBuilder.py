from AM2S.identity.Credentials import Credentials
from AM2S.identity.Identity import Identity
from AM2S.misc.TomlLoader import TomlLoader
from AM2S.templates.Builder import Builder


class IdentityBuilder(Builder[Identity]):
	__config: TomlLoader

	def __init__(self, config: TomlLoader):
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
			),
		)
