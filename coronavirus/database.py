"""在fastapi里配置使用数据库""" 


# 需要实现安装pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 建立sqlite数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./coronavirus.sqlite3"
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database_name"


engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    # 由于sqlalchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可以使用，这个参数只能用在SQLite，在其他数据库不需要它。
    SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True, connect_args={"check_same_thread": False}
)

# 在SQLAlchemy中，crud都是通过会话session进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库会话
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘，commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)


# 创建基本的映射类, 在models.py文件中导入
Base = declarative_base(bind=engine, name='Base')