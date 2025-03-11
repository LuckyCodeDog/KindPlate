
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q5560550@localhost/restaurantdb'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800  # 连接池回收时间（单位：秒）
