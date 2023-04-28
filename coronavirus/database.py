"""在fastapi里配置使用数据库""" 


# 需要实现安装pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 建立sqlite数据库，sqlite:///指定了使用SQLite数据库；./coronavirus.sqlite3指定了数据库文件的路径和名称。
SQLALCHEMY_DATABASE_URL = "sqlite:///./coronavirus.sqlite3"
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database_name"


engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    # 由于sqlalchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可以使用，这个参数只能用在SQLite，在其他数据库不需要它。
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

# 在SQLAlchemy中，crud都是通过会话session进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库会话
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘，commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)


# declarative_base函数创建了一个ORM基类，用于在应用程序中定义模型类，并将模型类与数据库表进行映射。
# 这个基类提供了一个元数据（metadata）属性，可以用来配置ORM映射的相关信息，如表名、列名、数据类型等
Base = declarative_base()