from urllib.parse import urlunparse, urljoin

from AM2S.presets.ScreenscraperEndpoint import ScreenscraperEndpoint
from AM2S.types.Identity import Identity


class ScreenscraperRequester:
    apiUrl: str
    identity: Identity
    endpoint: ScreenscraperEndpoint

    def __init__(self, identity: Identity, endpoint: ScreenscraperEndpoint):
        self.apiUrl = urlunparse(('https', "screenscraper.fr", "/api2/", "", "", ""))
        self.identity = identity
        self.endpoint = endpoint

    def getBaseQuery(self) -> dict[str, str]:
        return {
            "devid": self.identity.dev.login,
            "devpassword": self.identity.dev.password,
            "ssid": self.identity.account.login,
            "sspassword": self.identity.account.password,
            "softname": "AM2S",
            "output": "json"
        }

    def getRequestURL(self):
        return urljoin(self.apiUrl, self.endpoint)
