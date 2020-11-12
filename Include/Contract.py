# udp的合约
from json import loads

from Include.Path import Path


class Contract:
    clients = loads(Path('Bin/Config/UDPAccount.json').text())
