from sqlmodel import Session, SQLModel, create_engine
from app.config.database import config as database_config
from sqlalchemy.orm import sessionmaker
"""
DB连接池
"""
class ConnectionResolver:
    __default: str = 'default'
    __connections = {}

    def __init__(self):
        for name, config in database_config.items():
            self.add_connect(name, config)

    def connect(self, name: str = None):
        name = self.__default if name is None else name
        return self.__connections[name] if self.hash_connect(name) else None

    def hash_connect(self, name: str) -> bool:
        return name in self.__connections

    # 追加连接池
    def add_connect(self, name: str, config):
        host = 'localhost' if config['host'] is None else config['host']
        port = 3306 if config['port'] is None else config['port']
        username = '' if config['username'] is None else config['username']
        password = '' if config['password'] is None else config['password']
        database = '' if config['database'] is None else config['database']
        pool = {
            "pool_pre_ping": False if config['pool']['pool_pre_ping'] is None else config['pool']['pool_pre_ping'],
            "pool_size": 1 if config['pool']['pool_size'] is None else config['pool']['pool_size'],
            "max_overflow": 5 if config['pool']['max_overflow'] is None else config['pool']['max_overflow'],
            "pool_timeout": 20,
        }
        try:
            engine_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
            engine = create_engine(engine_url, pool_pre_ping=pool['pool_pre_ping'], pool_size=pool['pool_size'],
                                   max_overflow=pool['max_overflow'], pool_timeout=pool['pool_timeout'])
            self.__connections[name] = sessionmaker(bind=engine, expire_on_commit=True)
        except Exception as e:
            pass

    # 获取默认引擎
    def get_default_connect(self):
        return self.__default

    # 设置默认引擎
    def set_default_connect(self, name: str):
        self.__default = name