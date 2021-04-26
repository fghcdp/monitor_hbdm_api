import sys
sys.path.append('..')

from huobi_api.ws import *
from log.logger import *
from postgre.config import *
from postgre.connect import *


class Heartbeat():
    def __init__(self, db_name: str, tb_name: str):
        flag = self.__class__.__name__
        self._ftws = Ws(flag, '/center-notification')
        self._csws = Ws(flag, '/center-notification')
        self._usws = Ws(flag, '/center-notification')

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
        self._con.execute(f'delete from {self._tb}', be_read=False)

        # ws sub futures
        data = {"op": "sub",
                "topic": "public.futures.heartbeat"
                }
        self._ftws.sub(data, self.call_back)

        # ws sub swap
        data = {"op": "sub",
                "topic": "public.swap.heartbeat"
                }
        self._csws.sub(data, self.call_back)

        # ws sub u swap
        data = {"op": "sub",
                "topic": "public.linear-swap.heartbeat"
                }
        self._usws.sub(data, self.call_back)
        return True, None

    def call_back(self, data: str):
        ts = data['ts']
        event = data['event']

        topic = data['topic'].split('.')
        contract_type = topic[1]

        heartbeat = data['data']['heartbeat']
        recovery_time = data['data']['estimated_recovery_time']
        
        ok, data = self._con.execute(f'insert into {self._tb}(contract_type, ts, event, heartbeat, recovery_time) values(%s, %s, %s, %s, %s)',
                                     [contract_type, ts, event, heartbeat, recovery_time], False)
        if not ok:
            logger.error(data)


if __name__ == '__main__':
    instance = Heartbeat('hbdm_api', 'heartbeat')
    ok,data = instance.run()
    if not ok:
        logger.error(data)
    time.sleep(60*10)
