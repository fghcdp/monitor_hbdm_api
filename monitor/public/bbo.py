import sys
sys.path.append('..')

from log.logger import *
from huobi_api.ws import *
from postgre.config import *
from postgre.connect import *


class Bbo():
    def __init__(self, db_name: str, tb_name: str, symbol: str = 'btc'):
        flag = self.__class__.__name__
        self._ftws = Ws(flag, '/ws')
        self._csws = Ws(flag, '/swap-ws')
        self._usws = Ws(flag, '/linear-swap-ws')

        self._con = self._con = Connect()
        self._db = db_name
        self._tb = tb_name
        self._symbol = symbol

    def run(self) -> tuple:
        '''
        return: (True, None)/(False, msg)
        '''

        # open db
        ok, data = self._con.open(
            self._db, config['postgre']['user_name'], config['postgre']['pass_word'])
        if not ok:
            return False, data

        # ws sub futures
        data = {"sub": f"market.{self._symbol}_cw.bbo"}
        self._ftws.sub(data, self.ftcall_back)

        # ws sub swap
        data = {"sub": f"market.{self._symbol}-usd.bbo"}
        self._csws.sub(data, self.cscall_back)

        # ws sub u swap
        data = {"sub": f"market.{self._symbol}-usdt.bbo"}
        self._usws.sub(data, self.uscall_back)

        return True, None

    def ftcall_back(self, data: str):
        self._call_back('futures', data)

    def cscall_back(self, data: str):
        self._call_back('swap', data)

    def uscall_back(self, data: str):
        self._call_back('linear-swap', data)

    def _call_back(self, contract_type: str, data: str):
        ts = data['ts']

        contract_code = data['ch'].split('.')[1]

        item = data['tick']
        data_ts = item['ts']
        mrid = item['mrid']
        bid1_p = item['bid'][0]
        bid1_v = item['bid'][1]
        ask1_p = item['ask'][0]
        ask1_v = item['ask'][1]

        ok, data = self._con.execute(f'insert into {self._tb}(contract_type, ts, contract_code, data_ts, mrid, bid1_p, bid1_v, ask1_p, ask1_v) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                     [contract_type, ts, contract_code, data_ts, mrid, bid1_p, bid1_v, ask1_p, ask1_v], False)
        if not ok:
            logger.error(data)


if __name__ == '__main__':
    instance = Bbo('hbdm_api', 'bbo')
    ok, data = instance.run()
    if not ok:
        logger.error(data)
    time.sleep(60*1)
