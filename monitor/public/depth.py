import sys
sys.path.append('..')

from huobi_api.ws import *
from log.logger import *
from postgre.config import *
from postgre.connect import *


class Depth():
    def __init__(self, db_name: str, tb_name: str, symbol: str = 'btc', ktype: str = 'step6'):
        flag = self.__class__.__name__
        self._ftws = Ws(flag, '/ws')
        self._csws = Ws(flag, '/swap-ws')
        self._usws = Ws(flag, '/linear-swap-ws')

        self._con = self._con = Connect()
        self._db = db_name
        self._tb = tb_name
        self._symbol = symbol
        self._type = ktype

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
        data = {"sub": f"market.{self._symbol}_cw.depth.{self._type}"}
        self._ftws.sub(data, self.ftcall_back)

        # ws sub swap
        data = {"sub": f"market.{self._symbol}-usd.depth.{self._type}"}
        self._csws.sub(data, self.cscall_back)

        # ws sub u swap
        data = {"sub": f"market.{self._symbol}-usdt.depth.{self._type}"}
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
        event = self._type

        contract_code = data['ch'].split('.')[1]

        item = data['tick']
        data_ts = item['id'] * 1000
        mrid = item['mrid']
        bid20_p = item['bids'][19][0]
        bid20_v = item['bids'][19][1]
        ask20_p = item['asks'][19][0]
        ask20_v = item['asks'][19][1]
        
        ok, data = self._con.execute(f'insert into {self._tb}(contract_type, ts, event, contract_code, data_ts, mrid, bid20_p, bid20_v, ask20_p, ask20_v) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    [contract_type, ts, event, contract_code, data_ts, mrid, bid20_p, bid20_v, ask20_p, ask20_v], False)
        if not ok:
            logger.error(data)

if __name__ == '__main__':
    instance = Depth('hbdm_api', 'depth')
    ok,data = instance.run()
    if not ok:
        logger.error(data)
    time.sleep(60*10)
