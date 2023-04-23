from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String, DateTime, Date,func
from sqlalchemy.orm import relationship

from .database import Base


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
    __mapper_args__ = {"order_by": country_code} # 默认为倒序
    # __mapper_args__ = {"order_by": country_code.desc()} # 倒序则加上.desc()方法

    def __repr__(self):
        return f'{self.country}_{self.province}'
    
class Data(Base):
    pass