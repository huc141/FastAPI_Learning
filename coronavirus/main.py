from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from coronavirus import crud, schemas, models
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data
from typing import List
from pydantic import Field

"""集成和使用我们之前创建的所有其他部分"""

models.Base.metadata.create_all(bind=engine)

application = APIRouter()

# get_db: 该函数实现了一个数据库连接的上下文管理器，它返回一个通过 SessionLocal() 函数创建的本地数据库连接。
# 在这个示例中，使用了 yield 关键字来创建一个 Python 生成器对象，以便在请求处理期间使用数据库连接。
# 当请求处理完毕后，将自动关闭该数据库连接。
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
在 FastAPI 中，HTTP 请求体中的数据可以通过请求处理函数（decorated function）的参数来获取。
当我们在请求处理函数的参数中声明了一个 Pydantic 模型（例如这里的 `city: schemas.CreateCity`），
FastAPI 会自动从 HTTP 请求体中解析出这个模型所对应的 JSON、表单数据、文件等格式的数据，
然后将其转换为 Python 对象，并将其传入请求处理函数中。

具体来说，在这个代码示例中，`create_city` 函数的 `city` 参数被声明为 `schemas.CreateCity` 类型，
因此当有 POST 请求发送到 `/create_city` 路由时，FastAPI 会自动从 HTTP 请求体中解析出对应的 JSON 数据，
并根据 `schemas.CreateCity` 类型的定义，将其转换为一个 Python 对象。
这个 Python 对象就是请求处理函数 `create_city` 中的 `city` 参数所代表的值。
"""
# db: Session 表示这个参数的名称为 db，类型为 Session。Session 是一个数据库会话对象，
# 用于在数据库中执行查询和更新操作。= 号后面的部分 Depends(get_db) 表示这个参数将会使用 get_db() 函数的返回值作为值，也就是会话对象。
@application.post("/create_city",response_model=schemas.ReadCity)
def create_city(city:schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(name=city.province, db=db)
    if db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="城市已存在/已注册！")
    return crud.create_city(db=db, city=city)


@application.get("/get_city/{city}", response_model=schemas.ReadCity)
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到该城市！")
    return db_city


# response_model=List[schemas.ReadCity] 表示响应将是一个 List 类型，其中包含多个 ReadCity 类型的对象。
# List 是一个 Python 内置的类，可以用于包含多个相同类型的对象。
# 在这里，我们将 List 应用于 ReadCity 类型，因此响应将是一个 ReadCity 对象列表
@application.get("/get_cities", response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@application.post("/create_data", response_model=schemas.ReadData)
def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到该城市！")
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data


@application.get("/get_data")
def get_data(city: str = None, skip: int = 0, limit: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return data

