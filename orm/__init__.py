from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

from conf import s

base = declarative_base()

engine = create_engine(
    s.get_conf_str(
        "DB_URL", default="sqlite:///gateway.vdb?check_same_thread=false"
    ),
    poolclass=SingletonThreadPool,
    pool_size=128,
    pool_recycle=3600,
    # pool_use_lifo=True,
    pool_pre_ping=True,
    # max_overflow=-1,
)

base.metadata.create_all(engine)

s.init_db(engine)
