from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#功能:创建数据库表格，初始化数据库

#定义引擎
engine = create_engine('mysql+mysqlconnector://root:001233@192.168.0.168:3306/kuaik')
#绑定元信息
metadata = MetaData(engine)

#创建表格，初始化数据库
user = Table('resource', metadata,
    Column('id', Integer, primary_key = True),
    Column('subject', String(20)),
    Column('publish', String(40)),
    Column("material",String(40)),
    Column("grade",String(2)),
    Column("version",String(20)))

#创建数据表，如果数据表存在则忽视！！！
metadata.create_all(engine)

#获取数据库链接，以备后面使用！！！！！
# conn = engine.connect()