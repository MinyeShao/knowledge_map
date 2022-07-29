# --coding:utf-8--

from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool
import time


class SingletonMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance


class NebulaClient(metaclass=SingletonMeta):
    def __init__(self):
        self.client_pool = self.client()

    def client(self):
        _config = Config()
        _config.max_connection_pool_size = 250
        connection_pool = ConnectionPool()
        connection_pool.init([("172.31.252.39", 9669)], _config)

        return connection_pool

    def insert_entity(self, insert_params, ngql):
        with self.client_pool.session_context('root', 'nebula') as session:
            session.execute('USE knowledge_map;')
            insert_params_str = ", ".join(insert_params)
            ngql = f"{ngql}{insert_params_str}"
            resp = session.execute(ngql)

        return resp.error_code(), resp.error_msg()

    def del_entity(self, del_params, ngql1, ngql2):
        with self.client_pool.session_context('root', 'nebula') as session:
            session.execute('USE knowledge_map;')
            del_params = ", ".join(del_params)
            ngql = f"{ngql1}{del_params}{ngql2}"
            resp = session.execute(ngql)
        return resp.error_code(), resp.error_msg()

    def go_company_relationship(self, vid: str):
        with self.client_pool.session_context('root', 'nebula') as session:
            session.execute('USE knowledge_map;')
            ngql = 'go 1 to 3 steps from "%s" over * bidirect  where $^.person.name is not EMPTY or $$.person.name ' \
                   'is not EMPTY yield DISTINCT shareholder._src, shareholder._dst,shareholder._type, shareholder.ratio,' \
                   'shareholder.shareholder_type,shareholder.capital,executive._src,executive._dst,' \
                   'executive._type,executive.position, $^.person.name, $$.person.name' % (vid)
            resp = session.execute(ngql)
        return resp

    def match_company_relationship(self, ngql):
        try:
            with self.client_pool.session_context('root', 'nebula') as session:
                session.execute('USE knowledge_map;')
                ngql_all = 'match p=(v:company{hid:"%s"})-[*0..4]-() return p limit 10000' % (ngql)
                resp = session.execute(ngql_all)
        except Exception as e:
            print("sleep 20 seconds")
            time.sleep(20)
            resp = self.match_company_relationship(ngql)
        return resp


nebula = NebulaClient()
