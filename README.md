# 项目启动说明

1.安装依赖

```shell
pip install -r requirements.txt
```

2.初始化数据库，需要执行database_init.sql脚本

3.配置config.py文件，将数据库连接修改为本地对应的连接：

```python
import os
class Config:

    """基础配置"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "web3_card")  

    """数据库配置"""
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'      #改
    MYSQL_PASSWORD = 'root'  #改
    MYSQL_DB = 'web3-business-card'  #改
```

4.运行项目，进入主目录web3-business-card-backend/下执行：

```sh
python run.py
```

## 注意

目前所有接口的jwt验证已关闭，无需完成钱包签名验证即可直接调用接口进行测试，后续功能验证通过后须打开jwt验证

## 2025.3.22更新

- ### 数据库更新：需要运行database_update_1.sql脚本对数据库表进行修改

- ### 功能更新：主要更新了名片分享、数字资产录入与管理、用户反馈功能的接口，详见接口文档v1.2
