import sys
import time
from threading import Thread
sys.path.append('..')

from log.logger import *
from postgre.config import *
from postgre.connect import *


def _clear_thread(db_name: str, tb_names: list, before_minutes: int):
    con = Connect()
    ok, data = con.open(
        db_name, config['postgre']['user_name'], config['postgre']['pass_word'])
    if not ok:
        logger.error(data)
        return

    while True:
        for item in tb_names:
            cmd = f"delete from {item} where created_at >= current_timestamp - interval '{before_minutes} minutes'"
            ok, data = con.execute(cmd, None, False)
            if not ok:
                logger.error(data)
            logger.info(cmd)

        time.sleep(60*before_minutes)


def run_clear_public():
    db_name = 'hbdm_api'
    tb_names = ['bbo', 'depth', 'domain', 'funding_rate',
                'heartbeat', 'kline', 'settlement']
    before_minutes = 60*8
    t = Thread(target=_clear_thread, daemon=True,
               args=(db_name, tb_names, before_minutes))
    t.start()


if __name__ == '__main__':
    run_clear_public()
    while True:
        time.sleep(1)
