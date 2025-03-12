from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
mysql = MySQL(app)


# 初始化扩展
CORS(app)  # 允许跨域
JWTManager(app)  # 初始化 JWT

# 注册路由
from app.bpurl import auth_bp, user_bp, businessCard_bp

# 导入路由定义
# 确保在注册蓝图前导入路由定义
from app.handler import hd_auth
from app.handler import hd_user
from app.handler import hd_businesscard


app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(businessCard_bp)

# from app import routes  # 导入 API 路由

from flask import jsonify

# 全局异常处理
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"code": 500, "message": f"Internal Server Error: {str(e)}"}), 500


# def create_app():
#     """创建 Flask 应用"""
#     app = Flask(__name__)
#     app.config.from_object(Config)

   
    

#     return app


