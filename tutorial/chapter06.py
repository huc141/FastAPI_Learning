from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

app06 = APIRouter()

"""OAuth2密码模式和FastAPI的OAuth2PasswordBearer"""

"""
OAuth2PasswordBearer是接收URL作为参数的一个类：客户端会向该URL发送username和password参数，然后得到一个token值
OAuth2PasswordBearer并不会创建相应的URL路径操作，只是指明客户端用来请求Token的URL地址
当请求到来的时候，FASTAPI会检查请求的Authorization头信息，如果没有找到Authorization头信息，
或者头信息的内容不是Bearer token，它会返回401状态码（unauthorized）
"""
# 创建一个 OAuth2PasswordBearer 实例，指定 token URL。这里指定的 /token 是一个路由，该路由用于接收用户提供的用户名和密码，并返回访问令牌，以用于后续的授权访问。
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chatpter06/token") # 请求token的URL地址 http://127.0.0.1:8000/chatpter06/token

@app06.get("/oauth2_password_bearer")
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
    return {"token": token}


"""基于password和bearer token的oauth2 认证"""

# 用字典模拟一个存储了账户和密码的数据库
fake_users_db = {
    "johnsnow": {
        "username": "johnsnow",
        "full_name": "JohnSnow",
        "email": "johnsnow@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

# 模拟对密码的hash加密
def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 模拟对获取的token进行解码校验
def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的授权认证！",
            headers={"WWW-Authenticate": "Bearer"}, # OAuth2的规范，如果认证失败，请求头中返回“Authenticate”
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="当前用户未激活！")
    return current_user


@app06.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()): # form_data 是一个 OAuth2PasswordRequestForm 类型的参数，它被声明为一个依赖项（dependency），作为一个 API 路由函数的参数，用于处理登录请求。它包含了登录请求中的用户名和密码等敏感信息，由 FastAPI 的内置解析器将它们从请求中提取并转换为 OAuth2PasswordRequestForm 对象。
    user_dict = fake_users_db.get(form_data.username) # get()是字典的一个方法，它从字典中获取一个键的值，如果该键的值不存在于字典中，则返回None。在这里，form_data.username表示表单数据中的用户名。如果该用户名存在于fake_users_db中，那么user_dict将包含该用户的字典，包括该用户的用户名、完整名称、电子邮件地址、散列密码和是否已禁用的状态。如果该用户名不存在于fake_users_db中，那么将引发一个HTTP异常并返回一个错误消息。
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效的用户名或密码！")
    user = UserInDB(**user_dict)
    print("---------------")
    print(user)
    print("---------------")
    # user = UserInDB(username=user_dict['username'], email=user_dict['email'], full_name=user_dict['full_name'], disabled=user_dict['disabled'], hashed_password=user_dict['hashed_password'])
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效的用户名或密码！")
    return {"access_token": user.username, "token_type": "bearer"}


@app06.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user