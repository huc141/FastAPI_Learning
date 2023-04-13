from fastapi import APIRouter, Depends
from typing import Optional


app05 = APIRouter()

"""Dependencies 创建、导入和声明依赖"""
"""把函数作为依赖"""
# common_parameters 函数：这个函数定义了三个参数，question，page 和 limit。question 是一个可选参数，可以是任何字符串，
# page 和 limit 都是整数，它们的默认值分别是 1 和 100。当调用 common_parameters 函数时，它会返回一个包含这三个参数的字典。
async def common_parameters(question: Optional[str] = None, page: int = 1, limit: int = 100):
    return {"question": "question", "page": page, "limit": limit}

# dependency01 和 dependency02 函数：这两个函数是路由处理函数，使用 FastAPI 的 @app05.get 装饰器来定义 HTTP GET 请求。
# 这两个函数的唯一区别是它们的路径不同。这两个函数都接受一个名为 commons 的参数，
# 这个参数是通过 Depends 从 common_parameters 函数中注入的。
@app05.get("/dependency01")
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons

# Depends：这是一个 FastAPI 提供的函数，它用于依赖注入。当一个函数需要依赖另一个函数时，可以使用 Depends 来注入依赖函数的返回值。
# 在这个例子中，dependency01 和 dependency02 函数都需要 common_parameters 函数返回的字典，
# 因此它们都使用 Depends(common_parameters) 来注入这个依赖。
@app05.get("/dependency02")
async def dependency02(commons: dict = Depends(common_parameters)):
    return commons


"""把类作为依赖项"""
# 这一行定义了一个名为 fake_item_db 的变量，它是一个包含字典对象的列表。每个字典对象包含一个键 item_name 和对应的值。
# 这个变量被用作在路由处理函数中返回的示例数据。
fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, question: Optional[str] = None, page: int = 1, limit: int = 100):
        self.question = question
        self.page = page
        self.limit = limit

@app05.get("/classes_as_dependencies")
# 第一种将类作为依赖项的方法(三种方法效果都一样)
# async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams)):

# 第二种方法：
# async def classes_as_dependencies(commons: CommonQueryParams = Depends()):

# 第三种方法：
# 这段代码定义了一个名为 classes_as_dependencies 的路由处理函数，并将其映射到 URL 路径 /classes_as_dependencies。
# 这个函数的参数 commons 使用了 FastAPI 提供的 Depends 类型作为注入器，并将 CommonQueryParams 类型作为其参数。
# 这表示在调用路由处理函数时，FastAPI 会自动创建一个 CommonQueryParams 类型的实例，
# 以获取查询参数并将其作为 commons 参数传递给路由处理函数。
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {} # 在函数内部，它首先创建一个空的字典 response。
    if commons.question: # 然后，它检查 commons.question 是否存在。commons.question 实际上是 CommonQueryParams 类的一个属性，代表查询参数 question 的值。如果 commons.question 存在，它会将一个新键值对 {"question": commons.question} 添加到 response 字典中。
        response.update({"question": commons.question})
    # 这行代码使用了 Python 的列表切片操作，从 fake_item_db 列表中获取一个子列表。切片操作的语法是 list[start:end]，
    # 其中 start 是开始索引，end 是结束索引（不包括该索引对应的元素）。如果省略 start，则默认为 0，如果省略 end，则默认为列表的长度。
    # 在这个代码中，commons.page 和 commons.limit 是从 CommonQueryParams 类的实例中获取的属性值，
    # 它们分别代表分页查询的起始页码和每页显示的记录数。因此，fake_item_db[commons.page: commons.page + commons.limit] 
    # 就是从 fake_item_db 列表中获取一个子列表，该子列表包含从第 commons.page 页开始，往后 commons.limit 条记录。
    # 例如，如果 commons.page 的值为 1，commons.limit 的值为 2，那么这行代码将返回 fake_item_db 列表中的第 2 和第 3 条记录，
    # 即 {"item_name": "Bar"} 和 {"item_name": "Baz"}。如果 commons.page 的值为 0，commons.limit 的值为 1，
    # 那么这行代码将返回 fake_item_db 列表中的第 1 条记录，即 {"item_name": "Foo"}。
    items = fake_item_db[commons.page: commons.page + commons.limit]
    response.update({"items": items})
    return response

