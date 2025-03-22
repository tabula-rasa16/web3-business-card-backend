import os


class Config:

    BASE_URL = "http://localhost:5000"  # 本地开发环境路径

    """基础配置"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "web3_card")  # JWT 密钥


    """数据库配置"""
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'web3-business-card'


class DevelopmentConfig(Config):
    BASE_URL = "http://localhost:5000"   # 测试环境路径
