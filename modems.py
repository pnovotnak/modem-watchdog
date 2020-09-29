import requests
from bs4 import BeautifulSoup


class Modem:
    def __init__(self, username: str, password: str, url: str = "http://192.168.100.1"):
        self.session = requests.session()
        self.url = url
        self.username = username
        self.password = password

    def reboot(self):
        raise NotImplementedError

    def name(self) -> str:
        raise NotImplementedError


class NetgearCM1100(Modem):
    def _login(self):
        login_form = self.session.get(f'{self.url}/GenieLogin.asp')
        login_form.raise_for_status()
        bs = BeautifulSoup(login_form.text, 'html.parser')
        token = bs.find(attrs={'name': 'webToken'}).get('value', None)
        assert token is not None
        login = self.session.post(f'{self.url}/goform/GenieLogin', {
            "loginUsername": self.username,
            "loginPassword": self.password,
            "webToken": token,
            "login": 1,
        })
        login.raise_for_status()

    def _reboot(self):
        reboot_page = self.session.get(f'{self.url}/Reboot.asp')
        reboot_page.raise_for_status()

    def reboot(self):
        self._login()
        self._reboot()

    def name(self):
        return 'Netgear CM1100'
