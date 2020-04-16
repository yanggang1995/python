# _*_ coding:UTF-8 _*_

from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
import pandas as pd
# Presto
engine = create_engine('presto://host:port/hive/my_schema')  # host是服务器ip，port是端口，hive指的是Presto的catalog，my_schema是hive的schema。
df = pd.read_sql("select * from test", engine) # 和一般pandas从数据库中读取数据无任何区别，分析师们应该非常熟悉了。
print(df)
