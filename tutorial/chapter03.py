"""本章讲解：请求参数和验证，对于输入的部分，前端传递给后端的数据，我们如何去解析和验证"""

from fastapi import APIRouter, Path, Query
from enum import Enum
from typing import Optional, List

# 创建了一个 FastAPI 中的路由器对象，名称为 app03。
# APIRouter 类是 FastAPI 中用于创建路由器对象的类。路由器对象是一个包含多个路由的集合，可以用来组织和管理应用程序的路由。
# 在这个代码中，APIRouter() 创建了一个新的路由器对象，并将其赋值给 app03 变量。可以使用 app03 变量来定义路由器中的路由。
app03 = APIRouter()

"""1、路径参数和数字验证"""

# 函数的顺序就是路由的顺序
@app03.get("/path/parameters")
def path_params01():
    return {"message": "This is a message"}


@app03.get("/path/{parameters}")
def path_params01(parameters: str):
    return {"message": parameters}


# 定义一个名为CityName的枚举类，它继承了Python自带的str类和FastAPI框架中的Enum类。
# CityName枚举类定义了两个城市名及其所在国家的字符串常量，即Beijing = "Beijing China"和Shanghai = "Shanghai China"。
class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"

# @app03.get("/enum/{city}")是一个路由装饰器，它表示该函数对应于/enum/{city}这个URL地址，
# 其中的{city}表示一个路径参数。当向该URL发送GET请求时，FastAPI框架将会调用该函数进行处理，
# 函数中的参数city将会被绑定为URL路径中的{city}值。
@app03.get("/enum/{city}") # 枚举类型参数
async def latest(city: CityName): #async def latest(city: CityName)定义了一个名为latest的异步函数，它的参数city是一个枚举类型的参数，其取值必须是CityName类中定义的枚举值之一。函数的返回值是一个字典类型，包含了对应城市的一些数据信息，如确诊病例数和死亡人数等。
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1492, "death": 7}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 971, "death": 9}
    return {"city_name": city, "latest": "unknown"}

# 包含路径的路径参数转换
@app03.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {" The file_path is :": file_path}


# 使用fastapi中的Path类来对路径参数做验证（常用）
# 路径参数 number 通过 Path 类进行校验。... 表示这是一个必填参数，
# title 是参数的标题，description 是参数的描述。
# ge=1 表示参数的最小值为 1，le=10 表示参数的最大值为 10。
# 如果传入的参数不符合规定的类型或者校验条件，FastAPI 会返回一个 HTTP 异常，如 422 Unprocessable Entity。
# 否则，路由处理函数会返回一个 JSON 格式的响应，其中包含传入的参数 number。
@app03.get("/path_/{number}")
def path_params_validate(number: int = Path(..., title="Your number", description="这是中文描述", ge=1, le=10)):
    return {"Your number is:": number}


"""2、查询参数和字符串验证"""

@app03.get("/query")
def page_limit(page: int=1, limit: Optional[int]=None): # 给了默认值就是选填的参数，没给默认值则是必填参数
    if limit:
        return {"page":page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion")
def type_conversion(param: bool = False):   # bool类型转换：yes、on、1、True，则返回True；no、off、0、false，则返回False
    return param


@app03.get("/query/validations")
def query_params_validate( #该接口需要接受两个查询参数：value 和 values，这两个参数都使用了 FastAPI 中的 Query 方法来指定参数的元数据和验证规则。
    value: str = Query(..., min_length=8, max_length=16, regex="^a"), # value 参数使用了 Query 方法指定了以下元数据和验证规则：... 表示该参数是必须的，如果没有提供该参数则会返回 422 错误码；min_length=8 表示该参数的最小长度为 8；max_length=16 表示该参数的最大长度为 16；regex="^a" 表示该参数必须以字母 a 开头，否则会返回 422 错误码。
    values: List[str] = Query(default=["v1", "v2"], alias="alias_name") # values 参数使用了 Query 方法指定了以下元数据和验证规则：default=["v1", "v2"] 表示如果没有提供该参数，则默认为 ["v1", "v2"]；alias="alias_name" 表示该参数的别名为 alias_name，即在调用 API 时使用 alias_name 参数名来传递 values 参数。
):  
    return value,values #最后，该接口返回的是一个元组，包含了 value 和 values 两个参数的值。


"""请求体和字段"""
from pydantic import BaseModel, Field

class CityInfo(BaseModel):  # 定义了一个名为CityInfo的类，它继承了BaseModel，并使用Field对类属性进行了定义。CityInfo类有四个属性，分别为name、country、country_code、country_population。
    name: str = Field(..., example="Beijing")   # example是注解作用，值不会被验证。 name属性是一个字符串类型的必填字段，使用了Field来对其进行了定义
    country: str
    country_code: str = None # country_code还设置了默认值为None
    country_population: int = Field(default=800, title="人口数量", description="国家人口数量") # country_population则使用了Field来设定了一个默认值为800的整数类型字段，并给其定义了一个标题为人口数量、描述为国家人口数量的元数据信息。

# CityInfo类的Config属性中，使用schema_extra属性为该类增加了一个样例数据。这个样例数据是一个字典，包含了name、country、country_code和country_population四个字段
    class Config:
        schema_extra = {
            "example":{
            "name": "Shanghai",
            "country": "China",
            "country_code": "CN",
            "country_population": 140000001
            }
        }

# 最后，该程序定义了一个名为city_info的路由函数，该函数的参数city是一个CityInfo类型的对象，
# 通过print语句将其name和country两个属性的值打印到控制台，并将city对象转换成字典类型并返回。
@app03.post("/request_body/city")
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


"""花式传参：查询参数、路径参数、请求体的混合使用"""

@app03.put("/request_body/city/{name}") # 使用了 HTTP PUT 请求方法，处理 /request_body/city/{name} 的请求。
def mix_city_info(
        name: str, # 其中，name 是【路径参数】，使用字符串类型表示。
        city01: CityInfo, # city01 和 city02 是【请求体】中的 JSON 数据，使用 Pydantic 的 CityInfo 模型进行解析，如果无法解析为该模型，则会返回 422 Unprocessable Entity 错误。
        city02: CityInfo,
        confirmed :int = Query(ge=0,description="确诊数", default=0), # confirmed 和 death 是【查询参数】，使用了 FastAPI 的 Query 装饰器进行声明。其中，ge 表示大于等于，description 表示参数描述，default 表示参数默认值。
        death: int = Query(ge=0, description="死亡数", default=0)
):
    if name == "Shanghai":   # 该路由处理逻辑是，如果路径参数 name 为 "Shanghai"，则返回一个 JSON 对象，表示确诊数和死亡数。否则，返回两个 Pydantic 模型 city01 和 city02 的 JSON 形式。
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(),city02.dict()


"""花式传参：数据格式嵌套的请求体"""
from datetime import date


class Data(BaseModel):
    city: List[CityInfo] = None # 这里就是定义数据格式嵌套的请求体
    date: date
    confirmed: int = Field(ge=0, description="确诊数", default=0) # 在使用pydantic定义请求体数据的时候，要对字段进行校验，可使用Field类进行校验
    deaths: int = Field(ge=0, description="死亡数", default=0)
    recovered: int = Field(ge=0, description="痊愈数", default=0)

@app03.put("/request_body/nested")
def nested_models(data: Data):
    return data


"""设置cookie和Header参数"""
from fastapi import Cookie, Header


@app03.get("/cookie") # 效果只能用postman测试
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 在 FastAPI 中，可以通过 Cookie 函数来获取 cookie 的值。这个函数接受一个字符串类型的参数，用于指定要获取的 cookie 的名称。如果传入的 cookie 不存在，那么函数的返回值为 None。
    return {"cookie_id": cookie_id} # 通过将 cookie_id 参数指定为 Optional[str]，来表明这是一个可选的参数，也就是说，即使客户端没有传递 cookie_id 参数，我们的代码也不会报错。当然，如果客户端传递了 cookie_id 参数，我们的代码就可以通过 cookie_id 参数来获取传入的 cookie 的值了。


@app03.get("/header")
def header( # 通过 Header 函数来获取 Header 的值。这个函数接受两个参数，第一个是 Header 的名称，第二个是默认值。如果客户端没有传递这个 Header，那么函数的返回值就是默认值。
    user_agent: Optional[str] = Header(None, convert_underscores=True), # 将 user_agent 参数指定为 Optional[str] 类型，并通过 convert_underscores=True 参数来将 Header 名称中的下划线 _ 转换为连字符 -。
    x_token: List[str] = Header(None)
):
    """
    有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性，将下划线转为-
    :param user_agent: convert_underscores=True 会把user_agent转为user-agent
    :param x_token：x_token是包含多个值的列表
    :return:
    """
    return {"User-Agent": user_agent, "x_token": x_token}
