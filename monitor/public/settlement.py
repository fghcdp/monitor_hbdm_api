import sys
sys.path.append('..')

from huobi_api.ws import *
from log.logger import *
from postgre.config import *
from postgre.connect import *


class Settlement():
    def __init__(self, db_name: str, tb_name: str):
        flag = self.__class__.__name__
        self._ftws = Ws(flag, '/notification')
        self._csws = Ws(flag, '/swap-notification')
        self._usws = Ws(flag, '/linear-swap-notification')

        self._con = self._con = Connect()
        self._db = db_name
        self._tb = tb_name

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
        data = {"op": "sub",
                "topic": "public.*.contract_info"
                }
        self._ftws.sub(data, self.ftcall_back)

        # ws sub swap
        data = {"op": "sub",
                "topic": "public.*.contract_info"
                }
        self._csws.sub(data, self.cscall_back)

        # ws sub u swap
        data = {"op": "sub",
                "topic": "public.*.contract_info"
                }
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
        event = data['event']

        for item in data['data']:
            contract_code = item['contract_code']
            contract_status = item['contract_status']
            if 'settlement_time' in item:
                settlement_date = item['settlement_time']
            elif 'settlement_date' in item:
                settlement_date = item['settlement_date']
            
            ok, data = self._con.execute(f'insert into {self._tb}(contract_type, ts, event, contract_code, contract_status, settlement_date) values(%s, %s, %s, %s, %s, %s)',
                                        [contract_type, ts, event, contract_code, contract_status, settlement_date], False)
            if not ok:
                logger.error(data)

if __name__ == '__main__':
    instance = Settlement('hbdm_api', 'settlement')
    ok,data = instance.run()
    if not ok:
        logger.error(data)
    time.sleep(60*10)
