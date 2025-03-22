from flask import Blueprint




# 创建 Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
user_bp = Blueprint('user', __name__,url_prefix='/user')
businessCard_bp = Blueprint('businessCard', __name__,url_prefix='/businessCard')
digitalAsset_bp = Blueprint('digitalAsset', __name__,url_prefix='/digitalAsset')
feedback_bp = Blueprint('feedback', __name__,url_prefix='/feedback')