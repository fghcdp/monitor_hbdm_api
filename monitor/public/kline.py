import sys
sys.path.append('..')

from log.logger import *
from huobi_api.ws import *
from postgre.config import *
from postgre.connect import *


class Kline():
    def __init__(self, db_name: str, tb_name: str, symbol: str = 'btc', period: str = '1min'):
        flag = self.__class__.__name__
        self._ftws = Ws(flag, '/ws')
        self._csws = Ws(flag, '/swap-ws')
        self._usws = Ws(flag, '/linear-swap-ws')

        self._con = self._con = Connect()
        self._db = db_name
        self._tb = tb_name
        self._symbol = symbol
        self._period = period

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
        data = {"sub": f"market.{self._symbol}_cw.kline.{self._period}"}
        self._ftws.sub(data, self.ftcall_back)

        # ws sub swap
        data = {"sub": f"market.{self._symbol}-usd.kline.{self._period}"}
        self._csws.sub(data, self.cscall_back)

        # ws sub u swap
        data = {"sub": f"market.{self._symbol}-usdt.kline.{self._period}"}
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
        event = self._period

        contract_code = data['ch'].split('.')[1]

        item = data['tick']
        mrid = item['mrid']
        data_ts = item['id'] * 1000
        close = item['close']
        amount = item['amount']
        trade_turnover = close * amount

        ok, data = self._con.execute(f'insert into {self._tb}(contract_type, ts, event, contract_code, mrid, data_ts, close, amount, trade_turnover) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                     [contract_type, ts, event, contract_code, mrid, data_ts, close, amount, trade_turnover], False)
        if not ok:
            logger.error(data)


if __name__ == '__main__':
    instance = Kline('hbdm_api', 'kline')
    ok, data = instance.run()
    if not ok:
        logger.error(data)
    time.sleep(60*10)
