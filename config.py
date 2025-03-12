import os


class Config:

    """基础配置"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "web3_card")  # JWT 密钥


    """数据库配置"""
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'web3-business-card'
