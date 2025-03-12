from flask import request
from app import app
from app.common.tools import response,params_preprocess
from app.common.const import *

import random
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
from eth_account import Account
import datetime

from app.handler.hd_base import require

from app.bpurl import auth_bp

# Nonce 存储
NONCE_STORE = {}

@auth_bp.route("/getNonce", methods=["GET"])
def get_nonce():
    """生成随机 Nonce"""
    address = request.args.get("address")
    if not address:
        return response(code=400, message="error:地址不能为空")

    nonce = f"请签名以登录: {random.randint(100000, 999999)}"
    NONCE_STORE[address.lower()] = nonce
    return response(data={"nonce": nonce})


@auth_bp.route("/verifySignature", methods=["POST"])
@require("address", "signature")
def verify_signature():
    """验证签名并生成 JWT"""
    try:
        data = request.json
        data = params_preprocess(data)
        address = data.get("address")
        signature = data.get("signature")

        # if not address or not signature:
        #     return jsonify({"error": "参数错误"}), 400

        nonce = NONCE_STORE.get(address.lower())
        if not nonce:
            return response(code=400, message="error: Nonce 失效，请重试")

        # 签名验证
        message = encode_defunct(text=nonce)
        recovered_address = Account.recover_message(message, signature=signature)

        if recovered_address.lower() == address.lower():
            access_token = create_access_token(identity=address, expires_delta=datetime.timedelta(hours=JWT_TOKEN_EXPIRE_HOURS))
            del NONCE_STORE[address.lower()]  # 删除使用过的 Nonce
            return response(data={"token": access_token})

        return response(code = 401,message="error:签名验证失败")

    except Exception as e:
        return response(code=500, message=f"服务器错误: {str(e)}")