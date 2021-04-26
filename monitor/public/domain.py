import sys
import time
from threading import Thread
sys.path.append('..')

from huobi_api.rest import *
from log.logger import *
from postgre.config import *
from postgre.connect import *


class Domain():
    def __init__(self, db_name: str, tb_name: str, symbol: str = 'btc', period: str = '1min', sleep_second: int = 10*60):
        logger.info(self.__class__.__name__)
        self._domains = ['api.hbdm.com',
                         'api.hbdm.vn',
                         'api.btcgateway.pro']

        self._paths = {'futures': '/market/history/kline',
                       'swap': '/swap-ex/market/history/kline',
                       'linear-swap': '/linear-swap-ex/market/history/kline'}

        self._con = self._con = Connect()
        self._db = db_name
        self._tb = tb_name
        self._symbol = symbol
        self._period = period
        self._sleep_second = sleep_second

    def run(self) -> tuple:
        '''
        return: (True, None)/(False, msg)
        '''

        # open db
        ok, data = self._con.open(
            self._db, config['postgre']['user_name'], config['postgre']['pass_word'])
        if not ok:
            return False, data
        t = Thread(target=self._thread_fun, daemon=True)
        t.start()
        return True, None

    def _thread_fun(self):
        # rest req
        try:
            while True:
                # futures
                for item in self._domains:
                    ts = self._get_now_ts()
                    ok, data = get(item, self._paths['futures'], {'symbol': f'{self._symbol}_cw',
                                                                'period': self._period,
                                                                'size': 1})
                    if not ok:
                        logger.error(data)
                    else:
                        self._to_db(item, 'futures', ts, data)

                # swap
                for item in self._domains:
                    ts = self._get_now_ts()
                    ok, data = get(item, self._paths['swap'], {'contract_code': f'{self._symbol}-usd',
                                                        'period': self._period,
                                                        'size': 1})
                    if not ok:
                        logger.error(data)
                    else:
                        self._to_db(item, 'swap', ts, data)

                # u swap
                for item in self._domains:
                    ts = self._get_now_ts()
                    ok, data = get(item, self._paths['linear-swap'], {'contract_code': f'{self._symbol}-usdt',
                                                                'period': self._period,
                                                                'size': 1})
                    if not ok:
                        logger.error(data)
                    else:
                        self._to_db(item, 'linear-swap', ts, data)
                time.sleep(self._sleep_second)
        except Exception as e:
            logger.error(e)

    def _get_now_ts(self) -> int:
        ts = time.time()*1000
        return int(ts)

    def _to_db(self, domain: str, contract_type: str, local_ts: int, data: dict):
        data_ts = data['ts']

        contract_code = data['ch'].split('.')[1]

        ok, data = self._con.execute(f'insert into {self._tb}(contract_type, domain, event, contract_code, local_ts, data_ts) values(%s, %s, %s, %s, %s, %s)',
                                     [contract_type, domain, self._period, contract_code, local_ts, data_ts], False)
        if not ok:
            logger.error(data)


if __name__ == '__main__':
    instance = Domain('hbdm_api', 'domain')
    ok, data = instance.run()
    if not ok:
        logger.error(data)
    time.sleep(60*1)
