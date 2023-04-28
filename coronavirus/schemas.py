from pydantic import BaseModel
from datetime import datetime as date_
from datetime import datetime

"""建立与模型类对应的数据格式类"""

# 表示了新建数据时的输入格式，包含了对应的字段名和类型。
class CreateData(BaseModel):
    date: date_
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0

# 表示了新建数据时的输入格式，包含了对应的字段名和类型。
class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: int

# 用于查询数据时的返回格式
class ReadData(CreateData):
    id: int
    city_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True #orm_mode = True 指定了这些模型类的转换模式为 ORM 模式，即将查询到的数据转换为数据库模型类对象，以便于数据库的操作。这些模型的字段与数据模型类中的字段相对应，使其在转换时能够正确匹配。

# 用于查询数据时的返回格式
class ReadCity(CreateCity):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True