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

## 2025.4.1更新

- ### 依赖更新：新添加了moralis依赖，用于获取链上资产，需更新下依赖

- ### 数据库更新：新建了数据库表supported_chain需要运行database_update_2.sql脚本对数据库表进行修改

- ### 功能更新：主要更新了链上资产获取、数字资产录入功能的接口，详见接口文档v1.3与更新日志文档

## 2025.4.8更新

- ### 功能更新：更新了以下接口：

  - 1.上传图片（单张）
  - 2.批量上传文件
  - 3.上传视频（单个）
  - 4.回传图片/视频（用于前端展示）

## 2025.4.11更新

- ### 功能更新：主要更新了用户账户关注、贴子发布、朋友圈贴子展示、贴子点赞、评论、回复功能的接口，详见接口文档v1.4

## 2025.5.4更新

- ### 数据库更新:  digital_assets表新增字段chain_key, 需运行database_update_3.sql

- ### 接口更新：(详见更新日志文档)

  - 1.数字资产入库（单条）
  - 2.批量入库数字资产
  - 3.批量更新数字资产记录
  - 4.获取要展示的数字资产记录
