from sqlalchemy.orm import Session
from coronavirus import models, schemas


"""
编写可复用的函数用来与数据库中的数据进行交互。

CRUD分别为：增加、查询、更改和删除，即增删改查。
"""

# 这个函数根据给定的 city_id 查询城市数据表中对应的城市。db: Session 是一个依赖注入，它是 Session 类型的参数;city_id: int 是函数 get_city 的一个参数，它表示所查询的城市的 ID。
# db.query(models.City) 创建了一个 SQLAlchemy 查询对象，指定从 models.City 模型中查询数据。
# .filter(models.City.id == city_id) 添加了一个筛选条件，仅保留 id 字段等于 city_id 的记录。
# .first() 指定仅返回查询结果的第一个记录，如果没有结果则返回 None。因为 id 字段是唯一的，所以这种方式可以确保仅返回一个结果。
def get_city(db: Session, city_id: int): # 这里的 Session 类型表示与数据库的会话。在 FastAPI 中，通常使用 SQLAlchemy ORM 来连接数据库，Session 类型是 SQLAlchemy ORM 中用来管理数据库会话的对象。
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.province == name).first()


# skip和limit是可以由用户自定义的参数。在这个函数中，skip表示要跳过的行数，而limit表示要返回的最大行数。如果用户不指定这些参数，则函数会使用默认值skip=0和limit=10。
# .offset(skip) 方法用于设置查询偏移量，即跳过前 skip 条记录，这样可以支持分页查询。如果 skip 参数被省略，则默认为 0，从第一条记录开始查询。
# .limit(limit) 方法用于限制查询结果的数量，即最多返回 limit 条记录。如果 limit 参数被省略，则默认为 10。
# .all() 方法用于执行查询并返回查询结果的列表。
def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()


# 第二个参数city: schemas.CreateCity是一个Pydantic模型，包含了创建城市所需的数据，如城市名称，所属省份等。
def create_city(db: Session, city: schemas.CreateCity):
    # 使用city.dict将city对象转换为Python字典，并使用**操作符解包为关键字参数传递给models.City。这将创建一个City对象，其中的字段值将根据字典中的值进行设置。
    db_city = models.City(**city.dict())
    # 使用db.add()将City对象添加到数据库会话中
    db.add(db_city)
    db.commit() # db.commit()提交对数据库的更改，将新创建的城市记录保存到数据库中
    # 使用db.refresh()刷新City对象，以获取由数据库自动生成的ID等任何缺少的字段。这是必要的，因为当我们添加City对象时，ID是从数据库中自动生成的，而不是在city对象中提供的。
    db.refresh(db_city)
    # 返回新创建的City对象作为函数结果
    return db_city


def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
    # 通过 db 进行查询，使用 filter 方法根据 city 所属的省/直辖市来筛选出符合条件的数据，
    # models.Data.city.has(province=city)是一个过滤条件，表示查询Data表中的city字段的值，
    # 如果该字段的province属性的值等于传入的city参数，就将该数据加入结果集。
    # 其中has()方法表示查询Data表中的city字段，它是一个关系属性，
    # 因此可以通过该方法来查询城市的省份属性。
        return db.query(models.Data).filter(models.Data.city.has(province = city)).all()  # all() 方法会将查询结果封装为一个列表对象。
    return db.query(models.Data).offset(skip).limit(limit).all()


def create_city_data(db: Session, data: schemas.CreateData, city_id: int):
    db_data = models.Data(**data.dict(), city_id=city_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data