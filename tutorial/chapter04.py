"""本章讲解：响应模型示例"""

from fastapi import APIRouter,status, Form, File, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union


app04 = APIRouter()


"""响应模型"""
# 首先定义了一个 UserBase 类，作为 UserIn 和 UserOut 的基类
# UserBase 类中包含了 email、mobile、address 和 full_name 属性，这些属性都是 UserIn 和 UserOut 中所共有的,
# UserIn 和 UserOut 类分别继承 UserBase 类，并添加了它们各自所独有的属性。
class UserBase(BaseModel):
    email: EmailStr
    mobile: str = "1008611"
    address: str = None
    full_name: Optional[str] = None


class UserIn(UserBase):
    username: str
    password: str


class UserOut(UserBase):
    username: str


users = {
    "user01": {"username": "user01", "password": "123123", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "456456", "email": "user02@example.com", "mobile": "11111"},
}

# 使用 response_model 参数来指定 API 的响应模型，即为返回给客户端的数据结构。在下述代码中，使用 UserOut 作为响应模型，因此 API 的返回数据需要符合 UserOut 类型的结构。
# 具体来说，UserOut 继承自 UserBase，因此 UserOut 实例必须包含 UserBase 所有的字段，即 email、mobile、address 和 full_name。
# 此外，UserOut 还定义了一个额外的字段 username，因此返回的数据需要包含 username 字段。而由于 UserOut 继承自 UserBase，
# 因此返回的数据中也可能包含 UserBase 中定义的可选字段 address 和 full_name。
@app04.post("/respose_model", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """response_model_exclude_unset=True表示默认值不包含在响应中，仅包含实际给的值，如果实际给的值与默认值相同也会包含在响应中,
       例如，如果某个API返回的数据只需要包含某些属性，而其他属性可能是可选的，可以使用 response_model_exclude_unset=True 来只返回已经设置了值的属性，
       忽略那些没有值的属性。这样可以减小返回的数据大小，并且更加清晰地表达API的意图。
    """
    print(user.password)
    return users["user01"]


@app04.post("response_model/attributes", 
            # response_model = Union[UserIn, UserOut]
            # response_model_exclude=["password"]
            # response_model_include=["username","mobile","email"]
            response_model=List[UserOut]
            # response_model=UserOut
)  # Union用于取UserIn, UserOut的并集
async def response_model_attributes(user: UserIn):
    del user.password  # Union[UserIn, UserOut]后，删除password属性也可以返回成功,或者再路由中使用response_model_exclude=["password"]也可以排除返回password
    return user


"""响应状态码和status属性的调用"""
# 定义了一个HTTP POST请求的路由，该请求的路径是/status_code，并将响应状态码设置为200。
# 当这个路由被调用时，它将返回一个包含status_code字段的JSON响应，该字段的值为200。
# 这意味着，无论这个路由被调用的原因是什么，它都将返回HTTP状态码为200的响应。
@app04.post("/status_code", status_code=200)
async def status_code():
    return {"status_code": 200}

# 这个路由使用FastAPI框架提供的status模块中的一个常量HTTP_200_OK来设置响应状态码。
# 第一个路由使用了直接设置状态码的方式，而第二个路由使用了一个常量来设置状态码。
# 这两种设置状态码的方式在大多数情况下都是等效的，但是使用常量可以使代码更易于阅读和维护。
@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
    print(type(status.HTTP_200_OK))
    return {"status_code": status.HTTP_200_OK}


"""Form Data 表单数据处理"""
# 需要从 fastapi中导入Form, 
@app04.post("/login")
async def login(username: str=Form(...), password: str = Form(...)):
    """
    用Form类需要先pip install python-multipart,Form类的元数据和校验方法类似Body\Query\path\cookie
    ①username: str=Form(...)：这是函数的第一个参数，它使用了Python的类型提示语法，表明这个参数的类型是字符串类型。
    这个参数是通过表单提交的，并使用FastAPI框架提供的Form模块进行处理。...表示这个参数是必需的，如果请求中没有提供这个参数，那么将会引发一个HTTP异常。
    ②password: str = Form(...)：这是函数的第二个参数，它与username参数类似，也是通过表单提交的字符串类型参数。
    它也是必需的，如果请求中没有提供这个参数，将会引发一个HTTP异常。
    """
    return {"username": username}


"""Request Files 单文件、多文件上传以及参数详解"""

# 需要从fastapi中导入File, UploadFile
@app04.post("/file")
async def file_(file: bytes = File(...)): # 如果要上传多个文件 files: List[bytes] = File(...)
    """使用File类，文件内容会以bytes的形式读入内存，适合于上传小文件"""
    return {"file_size": len(file)}


@app04.post("/upload_files")
async def upload_files(files:List[UploadFile] = File(...)): # 如果要上传单个文件 file: UploadFile = File(...)
    """
        使用UploadFile类的优势：
            1、文件存储在内存中，使用的内存达到阈值后，将被保存在磁盘中
            2、适合于图片、视频大文件
            3、可以获取上传的文件的元数据、如文件名、创建时间等
            4、有文件对象的异步接口
            5、上传的文件是python文件对象，可以使用write()、read()、seek()、close()操作
    """
    results = []
    for file in files:
        contents = await file.read()
        print(contents)
    # return {"filename": files[0].filename, "content_type": files[0].content_type}
        results.append({"filename": file.filename, "content_type": file.content_type, "contents": contents, "size": file.size})
    return results


"""FastAPI项目的静态文件配置【见run.py文件】"""


"""Path Operation Configuration 路径操作配置"""

@app04.post(
    "/path_operation_configuration",
    response_model=UserOut, # response_model=UserOut：指定该函数的响应数据的数据模型为 UserOut。函数返回的数据将会被自动序列化为该数据模型的实例，并返回给客户端。如果响应数据无法序列化为该数据模型，则会抛出异常。
    summary="this is yulong summary", # 指定该函数的摘要为 this is yulong summary。摘要通常用于简短描述该函数的功能。
    description="this is yulong descriptiom", # 指定该函数的详细描述为 this is yulong description。详细描述通常用于提供更详细的说明，包括参数、返回值、异常等信息。
    response_description="this is yulong response_description", # 指定该函数响应的详细描述为 this is yulong response_description。响应描述通常用于提供有关响应的更详细说明，例如状态码的含义、响应头等信息。
    deprecated=False, # 指定该函数是否已被弃用。如果设置为 True，则表示该函数已被弃用；如果设置为 False，则表示该函数尚未被弃用。
    status_code=status.HTTP_200_OK # 指定该函数的默认状态码为 200。状态码用于表示服务器响应的状态，例如成功、失败等。
)
# 最后，该函数使用异步函数的方式进行定义，并且接受一个名为 user 的参数，其数据模型为 UserIn。函数体内，
# 该函数将 user 参数转化为字典，并返回该字典作为响应结果。
async def path_operation_configuration(user: UserIn):
    return user.dict()



"""应用常见的配置项【见run.py文件】"""


"""Handling Errors 错误处理"""

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id == 1:
        return {"item_id": item_id, "q": q}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
"""
HTTPException包含两个参数：status_code和detail。status_code表示HTTP状态码，detail是一个可选参数，表示错误的详细描述。如果不提供detail参数，FastAPI会默认使用与状态码相对应的描述。

在上面的例子中，如果传入的item_id不等于1，API将抛出一个404的HTTP异常，并返回一个描述“Item not found”的错误信息。如果不抛出HTTPException，FastAPI会默认返回500的HTTP异常，这样并不能很好地通知客户端发生了什么错误。

HTTPException可以让API更清晰地报告错误，同时也有助于客户端更好地理解发生了什么情况。
"""
