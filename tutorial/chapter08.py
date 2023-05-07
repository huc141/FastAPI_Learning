from fastapi import APIRouter, Depends

app08 = APIRouter()

"""[见run.py文件]Middleware 中间件"""

# 带yield的依赖，其退出部分的代码和后台任务会在中间件之后运行，
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
# 即finally部分的代码会在中间件之后运行


"""[见run.py文件]CORS跨域资源共享"""
# 域的概念：协议+域名+端口
