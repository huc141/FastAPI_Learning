# 首先，导入 FastAPI 和 Uvicorn 库。
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from tutorial import app03, app04, app05, app06, app07, app08


"""应用常见的配置项【见run.py文件】"""
# 接着，创建了一个名为 app 的 FastAPI 实例。并做了一下常用的配置项目
app = FastAPI(
    title="FastAPI 入门教程 and Coronavirus Tracker API Docs",
    description="FastAPI教程 新冠病毒疫情跟踪器API接口文档",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs"
)



"""FastAPI项目的静态文件配置【见run.py文件】"""
# mount挂载的概念：表示将某个目录下的一个完全独立的应用给挂载过来，这个不会在API交互文档中显示
app.mount(path='/coronavirus/static', app=StaticFiles(directory='./coronavirus/static'), name='static') # .mount()不要在分路由APIRouter().mount调用，模板会报错


# app03 表示一个 Router 对象，它包含了第三章中的多个路由。prefix='/chatpter03' 是一个可选参数，
# 用于指定将该路由器中的所有端点路由到应用程序中的某个子路径上。
# 例如，如果 prefix='/chatpter03'，则该路由器中的所有端点将被路由到应用程序的路径 '/chatpter03' 下。
# tags=['第三章 请求参数和验证'] 也是一个可选参数，用于为路由器中的所有端点指定一个或多个标签，以便于 OpenAPI 文档的生成和分类。
app.include_router(app03, prefix='/chatpter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chatpter04', tags=['第四章 响应处理和FASTAPI配置'])
app.include_router(app05, prefix='/chatpter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chatpter06', tags=['第六章 安全、认证和授权'])
app.include_router(app07, prefix='/chatpter07', tags=['第七章 FastAPI的数据库和多应用的目录结构设计'])
app.include_router(app08, prefix='/chatpter08', tags=['第八章 FastAPI'])

# 使用了 Uvicorn 的 run 方法来启动应用程序。
# run 方法接受一个字符串参数，指定了应用程序的入口点（在这里是 run.py 文件中的 app 实例），以及一些其他参数。
# 其中，host 参数设置为 0.0.0.0，表示应用程序将监听所有可用的网络接口，而不仅仅是本地主机。
# port 参数设置为 8000，指定了应用程序监听的端口号。
# reload 和 debug 参数分别用于开启热加载和调试模式。
# workers 参数指定了应用程序的工作进程数。
if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, workers=1)