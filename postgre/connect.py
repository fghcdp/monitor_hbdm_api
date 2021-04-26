import psycopg2
import psycopg2.extras
import sys


class Connect:
    def __init__(self):
        self._conn = None
        self._cursor = None

    def __del__(self):
        self.close()

    def open(self, db: str, name: str, pwd: str, host: str = '') -> tuple:
        '''
        return: (True, None)/(False, msg)
        '''

        if host == '':
            host = 'localhost'
        if db == '':
            db = 'postgre'

        conn_string = f"host='{host}' dbname='{db}' user='{name}' password='{pwd}'"

        try:
            self._conn = psycopg2.connect(conn_string)
            self._conn.set_session(autocommit=True)
            self._cursor = self._conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            return False, str(e)
        return True, None

    def close(self):
        if self._cursor is None:
            return
        self._conn.close()
        self._cursor = None

    def execute(self, cmd: str, params: list = None, be_read: bool = True) -> tuple:
        '''
        return: (True, data)/(False, msg)
        '''
        #print(cmd)
        #print(params)

        if self._cursor is None:
            return False
        try:
            self._cursor.execute(cmd, params)
            result = None
            if be_read:
                result = self._cursor.fetchall()
        except Exception as e:
            return False, str(e)
        return True, result


if __name__ == '__main__':
    pg = Connect()
    ok, data = pg.open('hbdm_api', 'hbdm_api', 'hbdm_api')
    if not ok:
        print('open db error:'+data)
        sys.exit(0)
    print('open db ok')
    ok, data = pg.execute('select * from test')
    print(ok, data)
