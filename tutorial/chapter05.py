from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional, Union


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


"""Sub-dependencies 子依赖项"""

# 定义了一个名为 query 的函数，它接受一个名为 q 的可选参数，该参数可以是字符串或 None 类型。如果没有提供 q 参数，则函数将返回 None。
def query(q: Union[str, None] = None):
    return q

# 定义了一个名为 sub_query 的函数，它使用 Depends 装饰器。这意味着它是一个依赖项函数，可以注入其他依赖项或参数。
# 在这个例子中，sub_query 函数依赖于 query 函数，并使用了 last_query 参数。
# query 参数被注入为一个可选参数，其类型可以是字符串或 None。如果请求中没有提供 q 参数，那么 query 参数将默认为 None。
# last_query 参数是一个可选的字符串，它的默认值是 None。如果 q 参数不是 None，那么 sub_query 函数将返回它。否则，如果 q 参数是 None，它将返回 last_query 参数的值。
def sub_query(q: str = Depends(query), last_query: Optional[str] = None): 
    if not q:
        return last_query
    return q

# sub_dependency 函数：这是一个名为 sub_dependency 的路由函数，它使用了 GET 方法，路径为 /sub_dependency。
# inal_query 是一个字符串类型的参数，它使用 Depends 类从名为 sub_query 的依赖项中获取。
# sub_dependency 函数，final_query 参数使用了 Depends 类，并指定了一个名为 sub_query 的依赖项。
# use_cache=True 意味着，如果已经计算了一次 sub_query 的值，则不必重新计算，直接返回缓存的结果即可。
# 最终，sub_dependency 函数返回一个字典，其中包含 "sub_dependency" 键和 final_query 的值。
@app05.get("/sub_dependency")
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    return {"sub_dependency": final_query}


"""路径操作装饰器依赖项"""
# 有时，我们并不需要在路径操作函数中使用依赖项的返回值。或者说，有些依赖项不返回值。但仍要执行或解析该依赖项。
# 对于这种情况，不必在声明路径操作函数的参数时使用 Depends，而是可以在路径操作装饰器中添加一个由 dependencies 组成的 list。
# 路径操作装饰器依赖项的执行或解析方式和普通依赖项一样，但就算这些依赖项会返回值，它们的值也不会传递给路径操作函数。

async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# 这个函数没有参数，因为它不需要从 HTTP 请求中获取任何信息。
# 在 dependencies 参数中，我们传递了两个依赖项：verify_token 和 verify_key。
# 这意味着在调用 read_items 函数之前，必须先调用这两个依赖项，并通过它们进行验证，否则会抛出 HTTP 异常。
# 最后，read_items 函数返回一个包含两个元素的列表，其中每个元素都是一个字典，代表两个不同的条目，
# 分别为 "item": "Foo" 和 "item": "Bar"。这些数据将作为 HTTP 响应返回给客户端。
@app05.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


"""全局依赖"""
# 使用场景：假设有一些依赖或者子依赖项需要提供给整个站点的所有应用程序，或者是在某一个子应用里面，能够被程序调用

# 在 dependencies 参数中，我们传递了两个依赖项：verify_token 和 verify_key。这意味着在调用 read_items 或 read_users 函数之前，
# 必须先调用这两个依赖项，并通过它们进行验证，否则会抛出 HTTP 异常。
app05 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


@app05.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app05.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


"""Dependencies with yield 带yield的依赖(需要python3.7版本)"""
# 以下是伪代码
async def get_db():
    db = "db_connection"
    try:
        yield db
    finally:
        db.endswith("db_close")

async def dependency_a():
    dep_a = "generate_dep_a()"
    try:
        yield dep_a
    finally:
        dep_a.endswith("db_close")


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = "generate_dep_b()"
    try:
        yield dep_b
    finally:
        dep_b.endswith(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = "generate_dep_c()"
    try:
        yield dep_c
    finally:
        dep_c.endswith(dep_b)
