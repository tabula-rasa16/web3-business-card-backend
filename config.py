import os


class Config:

    BASE_URL = "http://localhost:5000"  # 本地开发环境路径

    """基础配置"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "web3_card")  # JWT 密钥
    MORALIS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjVkMGIwM2M5LWY2OTctNGUwZC1iMDM1LTQzNjk0MGNhOTFiZCIsIm9yZ0lkIjoiNDM4NDcwIiwidXNlcklkIjoiNDUxMDkzIiwidHlwZUlkIjoiMDAxNTg3OGYtMTc3ZC00NWI0LWFmODItMTBkZWU0YTFlODBmIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NDMxNDk3ODIsImV4cCI6NDg5ODkwOTc4Mn0.KOGP5Yt1yUxes1ERrEMKcSZSN6m5LAA3EHKHbLcVFc0" # moralis api key


    """数据库配置"""
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'web3-business-card'


class DevelopmentConfig(Config):
    BASE_URL = "http://localhost:5000"   # 测试环境路径
