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

    """静态资源配置"""
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = 'uploads'
    IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, 'images')
    VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')
    # 创建目录（若不存在）
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(VIDEO_FOLDER, exist_ok=True)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 限制上传文件大小为50MB
    # 支持的文件格式
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}


class DevelopmentConfig(Config):
    BASE_URL = "http://localhost:5000"   # 测试环境路径
