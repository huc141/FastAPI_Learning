from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String, DateTime, Date,func
from sqlalchemy.orm import relationship

from .database import Base

# 创建City类，定义相关属性
class City(Base):
    __tablename__ = 'city' # 数据库的表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(100), nullable=False, comment='国家代码')
    country_population = Column(BigInteger, nullable=False, comment='国家人口')
    data = relationship('Data', back_populates='city') # Data是关联的类名，back_populates是来指定反向访问的属性名称

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='修改时间')

    # 获取到这张表的数据让其能够排序
    # __mapper_args__ = {"order_by": country_code} # 默认为倒序
    # __mapper_args__ = {"order_by": country_code.desc()} # 倒序则加上.desc()方法

    def __repr__(self):
        return f'{self.country}_{self.province}'

# 创建Data类，定义相关属性
class Data(Base):
    __tablename__ = 'data' # 数据库的表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市') # 注意大小写，ForeignKey里的字符串格式不是 类名.属性名，而是 表名.字段名
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    city = relationship('City', back_populates='data') # City是关联的上面的类名，back_populates来指定反向访问的属性名称

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='修改时间')

    # 获取到这张表的数据让其能够排序
    # __mapper_args__ = {"order_by": date.desc()} # 倒序则加上.desc()方法

    def __repr__(self):
        return f'{repr(self.date): 确诊{self.confirmed}}'
        # return f'{self.country}_{self.province}'


"""
在Python中，__repr__方法是一个特殊方法，用于返回一个对象的字符串表示形式。这个方法会在调用内置函数repr()时自动调用。它通常返回一个可打印的字符串，表示当前对象的属性值。

在上述代码中，两个ORM模型类 City 和 Data 都实现了 __repr__ 方法，用于在对象打印时展示其内容。

对于 City 类，它的 __repr__ 方法返回一个格式为 {country}_{province} 的字符串，其中 {country} 和 {province} 分别是对象的 country 和 province 属性值。这样可以让我们通过打印 City 对象来快速查看该对象所表示的省份和国家信息。

对于 Data 类，它的 __repr__ 方法返回一个包含数据日期和确诊数量的字符串。该方法使用了Python的内置 repr() 函数将日期格式化为可打印的字符串，并在字符串中包含了对象的 confirmed 属性值，表示当前数据的确诊数量。

在调试和开发过程中，实现 __repr__ 方法非常有用，因为它可以帮助我们快速了解对象的属性值，从而更好地理解代码的行为和逻辑。



这是 `Data` 类的 `__repr__` 方法的实现，其目的是为了返回一个可打印的字符串表示该对象的内容。

这个方法使用了Python中的格式化字符串，结合了内置函数`repr()`和对象的`date`和`confirmed`属性值，生成了一个类似于 `日期 确诊数量` 的字符串。

具体来说，`repr(self.date)` 将 `date` 属性转换为可打印的字符串，`:` 后的部分 `确定诊{self.confirmed}` 是格式化字符串的一部分，它表示将 `self.confirmed` 的值插入到字符串中，从而构成最终的打印字符串。

例如，如果 `Data` 对象的 `date` 属性是 2022-05-01，`confirmed` 属性是 12345，那么调用 `repr()` 方法后返回的字符串是 `'2022-05-01'`。此时，整个 `__repr__` 方法返回的字符串就是 `2022-05-01 确诊12345`。

通过实现 `__repr__` 方法，我们可以方便地在开发和调试过程中查看对象的内容，而不需要手动打印每一个属性。这可以大大提高我们的效率和代码质量。


"""