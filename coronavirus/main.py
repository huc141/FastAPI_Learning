from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from coronavirus import crud, schemas, models
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data
from typing import List

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


@application.get("/get_cities", response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@application.post("/create_data", response_model=schemas.ReadData)
def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data


@application.get("/get_data")
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return data

