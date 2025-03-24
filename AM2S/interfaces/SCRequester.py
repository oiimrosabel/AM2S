from abc import abstractmethod

from furl import furl

from AM2S.data.Identity import Identity
from AM2S.enums.ScreenscraperEndpoint import ScreenscraperEndpoint

baseUrl = 'https://api.screenscraper.fr/api2'


class SCRequester[T, V]:
    __identity: Identity
    __endpoint: ScreenscraperEndpoint

    def __init__(self, identity: Identity, endpoint: ScreenscraperEndpoint):
        self.__identity = identity
        self.__endpoint = endpoint

    def getRequestURL(self) -> furl:
        url = furl(baseUrl)
        url.set({
            "devid": self.__identity.dev.login,
            "devpassword": self.__identity.dev.password,
            "ssid": self.__identity.account.login,
            "sspassword": self.__identity.account.password,
            "softname": "AM2S",
            "output": "json"
        })
        url.path.segments.append(self.__endpoint)
        return url

    @abstractmethod
    def getData(self, element: T) -> V:
        pass
