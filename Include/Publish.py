import socket
from json import loads

import redis
from Include.Log import log
from Include.Path import Path


class Publish:
    def __init__(self):
        self.way = '0'
        self.tool = None

    def __config_tool(self):
        self.way = Path('Bin/Config/Publish.txt').text().strip()
        if self.way == '1':  # redis
            tool = self.__get_redis()

            def send(msg):
                chanel = ''.join(msg[:3])
                tool.publish(chanel, ','.join(msg))
        # names = [[f'QBidPrice{i}', f'QBidQty{i}', f'QAskPrice{i}', f'QAskQty{i}'] for i in range(1, 21)]
        # names = ['ExchangeNo', 'CommodityNo', 'Contract.ContractNo1', 'DateTimeStamp', 'QPreClosingPrice',
        #          'QPreSettlePrice', 'QPrePositionQty', 'QOpeningPrice', 'QLastPrice', 'QHighPrice', 'QLowPrice',
        #          'QHisHighPrice', 'QHisLowPrice', 'QLimitUpPrice', 'QLimitDownPrice', 'QTotalQty', 'QTotalTurnover',
        #          'QPositionQty', 'QAveragePrice', 'QClosingPrice', 'QSettlePrice', 'QLastQty', 'QImpliedBidPrice',
        #          'QImpliedBidQty', 'QImpliedAskPrice', 'QImpliedAskQty', 'QPreDelta', 'QCurrDelta', 'QInsideQty',
        #          'QOutsideQty', 'QTurnoverRate', 'Q5DAvgQty', 'QPERatio', 'QTotalValue', 'QNegotiableValue',
        #          'QPositionTrend', 'QChangeSpeed', 'QChangeRate', 'QChangeValue', 'QSwing', 'QTotalBidQty',
        #          'QTotalAskQty'] + [j for i in names for j in i]
        #
        # if self.way == '1':  # redis
        #     tool = self.__get_redis()
        #
        #     def send(msg):
        #         chanel = ''.join(msg[:3])
        #         content = {_name: _values for _name, _values in zip(names, msg)}
        #         tool.publish(chanel, dumps(content))

        elif self.way == '2':  # socket
            tool = self.__get_socket()

            def send(msg):
                tool.send(bytes(','.join(msg), encoding='gbk'))

        elif self.way == '3':  # 文本
            def send(msg):
                name = f"Bin//{''.join(msg[:3])}.txt"
                Path(name).write_text(','.join(msg))

        elif self.way == '4':  # udp
            clients = loads(Path('Bin/Config/UDPAccount.json').text())
            # 使用合约来确定客户ip，比如COMEXGC2009:101.0.0.0
            con2ip = {}
            for client, contracts in clients.items():
                client = client.split(',')
                client = client[0], int(client[1])

                for contract in contracts:
                    contract = contract.split(' ')
                    contract = contract[0] + contract[2] + contract[3]
                    if contract in con2ip.keys():
                        con2ip[contract].append(client)
                    else:
                        con2ip[contract] = [client]

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            def send(msg):
                contract = ''.join(msg[:3])
                for ip in con2ip.get(contract, []):
                    print(contract, ip)
                    s.sendto(','.join(msg).encode(), ip)

        else:
            send = print
        self.tool = send

    @staticmethod
    def __get_redis():
        redis_conf = {'socket_timeout': 3}
        for line in Path('Bin/Config/Redis.txt').lines():
            if ':' in line:
                _key, value = [j.strip() for j in line.split(':')]
                redis_conf[_key] = value if value != 'None' else None

        pool = redis.ConnectionPool(**redis_conf)
        r = redis.Redis(connection_pool=pool)
        log('start Redis->' + ','.join(redis_conf))

        return r

    @staticmethod
    def __get_socket():
        hostname, port = [i.strip() for i in Path('Bin/Config/Socket.txt').lines() if i.strip()]
        port = int(port)

        srv = socket.socket()  # 创建一个socket
        srv.bind(('', port))
        srv.listen(5)

        log(f"socket等待{hostname}:{port}的链接")

        connect_socket, addr = srv.accept()
        print('链接IP', addr)
        log(f"socket链接成功")
        return connect_socket

    def get_tool(self):
        self.__config_tool()
        return self.tool
