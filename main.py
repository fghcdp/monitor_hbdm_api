from monitor import public
from clear_db import utils
from log.logger import *
import time


def _run_instance(type_module: str, py_file: str, cls_name: str, db_name: str, tb_name: str):
    md_name = __import__(f'monitor.{type_module}.{py_file}',
                         globals(), locals(), [cls_name])
    if not hasattr(md_name, cls_name):
        logger.error(f'has not module: monitor.{py_file}.{cls_name}')
        return
    metename = getattr(md_name, cls_name)
    instance = metename(db_name, tb_name)
    ok, data = instance.run()
    if not ok:
        logger.error(data)

def _run_pub_monitor():
    modules = {'Bbo': 'bbo',
               'Depth': 'depth',
               'Domain': 'domain',
               'FundingRate': 'funding_rate',
               'Heartbeat': 'heartbeat',
               'Kline': 'kline',
               'Settlement': 'settlement'}
    for cls_name, tb_name in modules.items():
        _run_instance('public', tb_name, cls_name, db_name, tb_name)


if __name__ == '__main__':
    db_name = 'hbdm_api'
    _run_pub_monitor()
    utils.run_clear_public()
    while True:
        time.sleep(1)
