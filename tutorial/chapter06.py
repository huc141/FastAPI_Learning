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
# 创建一个 OAuth2PasswordBearer 实例，指定 token URL。这里指定的 /chatpter06/token 是一个路由，该路由用于接收用户提供的用户名和密码，并返回访问令牌，以用于后续的授权访问。
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

# 这个类定义了一个用户对象的数据模型，它包含了用户的用户名、电子邮件地址、全名和禁用状态。这个类继承自 Pydantic 的 BaseModel 类，这个类使我们可以方便地定义和验证数据模型。
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# 这个类是 User 类的子类，表示数据库中的用户对象。它包含了 User 对象的所有属性，并添加了一个哈希密码属性。
class UserInDB(User):
    hashed_password: str


@app06.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()): # form_data 是一个 OAuth2PasswordRequestForm 类型的参数，它被声明为一个依赖项（dependency），作为一个 API 路由函数的参数，用于处理登录请求。它包含了登录请求中的用户名和密码等敏感信息，由 FastAPI 的内置解析器将它们从请求中提取并转换为 OAuth2PasswordRequestForm 对象。
    # 它首先从 fake_users_db 数据库中获取一个字典，该字典的键是用户的用户名，并将其存储在名为 user_dict 的变量中。
    user_dict = fake_users_db.get(form_data.username) # get()是字典的一个方法，它从字典中获取一个键的值，如果该键的值不存在于字典中，则返回None。在这里，form_data.username表示表单数据中的用户名。如果该用户名存在于fake_users_db中，那么user_dict将包含该用户的字典，包括该用户的用户名、完整名称、电子邮件地址、散列密码和是否已禁用的状态。如果该用户名不存在于fake_users_db中，那么将引发一个HTTP异常并返回一个错误消息。
    # 如果用户名无效，则 user_dict 将是一个空值，因此代码将抛出 HTTPException 异常，HTTP 状态码为 400，详细信息为 "无效的用户名或密码！"。
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效的用户名或密码！")
    # 如果用户名有效，则使用 UserInDB 模型将 user_dict 转换为 UserInDB 对象。
    user = UserInDB(**user_dict)
    # user = UserInDB(username=user_dict['username'], email=user_dict['email'], full_name=user_dict['full_name'], disabled=user_dict['disabled'], hashed_password=user_dict['hashed_password'])
    print("---------------")
    print(user)
    print("---------------")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效的用户名或密码！")
    return {"access_token": user.username, "token_type": "bearer"}


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


@app06.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


"""开发基于JSON Web Tokens的认证 - OAuth2 实现密码哈希与 Bearer JWT 令牌验证"""
# 需要安装的包：pip install python-jose[cryptography]  pip install passlib[bcrypt]
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # 秘钥
ALGORITHM = "HS256" # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌的过期时间（分钟）

# .update() 是 Python 中字典的一个方法，用于更新字典中的数据。该方法接受一个字典作为参数，并将其合并到原始字典中。
# 如果参数字典中包含原始字典中已经存在的键，则会覆盖原始字典中的值，否则会将新的键值对添加到原始字典中。
# 例如，.update() 方法将更新原始的 fake_users_db 字典，将 "johnsnow" 用户的信息更新为指定的值。
# 如果该用户已经存在，则将覆盖其原有的信息。
fake_users_db.update({
    "johnsnow": {
        "username": "johnsnow",
        "full_name": "johnsnow",
        "email": "johnsnow@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
})

class Token(BaseModel):
    """返回给用户的Token"""
    access_token: str
    token_type: str

# 使用 CryptContext() 函数，该函数是由 passlib 库提供的密码管理库，用于提供密码处理和验证的相关功能。
# 指定哈希算法为 bcrypt，并将其作为参数传递给 schemes 参数。 bcrypt 是一种常用的密码哈希算法，可以生成安全且不可逆的哈希值。
# 将 deprecated 参数设置为 "auto"，表示使用所有已弃用的哈希算法，并在必要时自动迁移到更强大和更安全的哈希算法。
# 这样可以确保系统中使用的密码哈希算法始终是最新和最安全的。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/chatpter06/jwt/token")

# 该函数将两个参数 plain_password 和 hashed_password 作为输入，其中 plain_password 是明文密码，hashed_password 是哈希密码。
def verify_password(plain_password: str, hashed_password: str):
    """对密码进行校验"""
    # pwd_context.verify() 方法将明文密码 plain_password 和哈希密码 hashed_password 作为参数传递，该方法会将明文密码进行哈希处理，
    # 并与哈希密码进行比较。如果两者匹配，则返回 True，否则返回 False。
    return pwd_context.verify(plain_password, hashed_password)


def jwt_get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
# 用于验证用户是否已注册并且密码是否正确，username：用户名。password：用户输入的密码。
def jwt_authenticate_user(db, username: str, password: str):
    user = jwt_get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# 用于创建 JWT 认证的 token，expires_delta：token的过期时间，可选参数，默认为 15 分钟
def created_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # 将data字典参数复制到新的变量to_encode中，以便稍后将其编码为JWT。
    to_encode = data.copy()
    # 如果expires_delta存在，则表示需要设置访问令牌的过期时间。
    if expires_delta:
        expire = datetime.utcnow() + expires_delta # 使用当前时间和传递的expires_delta计算出访问令牌的到期时间。
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) # 如果expires_delta不存在，则将过期时间设置为15分钟。使用当前时间和15分钟计算出访问令牌的到期时间。
    to_encode.update({"exp": expire}) # 将到期时间添加到to_encode字典中，将其作为JWT有效负载的一部分。
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # 使用JWT库的encode函数，将to_encode字典编码为JWT字符串，并使用SECRET_KEY和ALGORITHM进行签名。
    return encoded_jwt  # 返回编码后的JWT字符串。


# token为请求头中的token，使用Depends进行依赖注入，即在函数调用时会自动注入oauth2_scheme。
async def jwt_get_current_user(token: str = Depends(oauth2_scheme)):
    # 用于在验证用户凭据失败时抛出异常。
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, # 设置HTTP状态码为401，表示未授权。
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 使用jwt.decode解码token，其中SECRET_KEY是用于加密和解密token的密钥，ALGORITHM是用于加密和解密的算法。
        # 从解码后的payload中获取sub字段的值，即用户的用户名。sub是payload中的一个标准声明，表示subject，即主题，
        # 它通常被用于指定JWT所代表的用户或其他实体。username就是作为JWT的subject来使用的，
        # 所以在获取用户信息时，需要从payload中获取username的值，即payload.get("sub")。
        username: str = payload.get("sub") 
        if username is None: # 如果用户名为空，说明没有找到对应的用户，抛出credentials_exception异常。
            raise credentials_exception
    except JWTError: # 如果解码token失败，说明token无效，抛出credentials_exception异常
        raise credentials_exception
    user = jwt_get_user(db=fake_users_db, username=username) # 获取用户名为username的用户。
    if user is None:
        raise credentials_exception
    return user # 如果一切正常，返回用户对象。


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app06.post("/jwt/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    user = jwt_authenticate_user(db=fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = created_access_token(
        data={"sub": user.username},
        expires_delta = access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app06.get("/jwt/users/me")
async def jwt_read_users_me(current_user: User = Depends(jwt_get_current_active_user)):
    return current_user
