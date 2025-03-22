from flask import request, jsonify
from app import app
# import models.users as users_db
import app.models.user_feedback as feedback_db
from app.common.tools import response, params_preprocess,generate_unique_id
from app.common.const import *

# import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import feedback_bp


# 创建用户反馈
@feedback_bp.route('/create', methods=['POST'])
# @jwt_required()
@require("user_id")
def create_feedback():
    data = request.json
    data = params_preprocess(data)
    feedback_db.add_user_feedback(data['user_id'], data.get('feedback_content'), data.get('rel_record_id'), data.get('satisfaction'))
    return response(message="Feedback created Success")


# 获取个人创建的用户反馈列表
@feedback_bp.route('/list/', methods=['GET'])
# @jwt_required()
def get_user_feedback_list():
    user_id = request.args.get("user_id")
    feedback_list = feedback_db. get_feedback_by_user_id(user_id)
    return response(data=feedback_list)


# 根据id获取单条反馈记录
@feedback_bp.route('/getRecord', methods=['GET'])
# @jwt_required()
def get_feedback_by_id():
    feedback_id = request.args.get("id")
    feedback = feedback_db.get_feedback_by_id(feedback_id)
    return response(data=feedback)


# 撤销用户反馈
@feedback_bp.route('/revoke', methods=['POST'])
# @jwt_required()
@require("id")
def revoke_feedback():
    data = request.json
    data = params_preprocess(data)
    feedback_db.update_user_feedback(data['id'], FEEDBACK_HANDLE_STATUS_REVOKE, remark=data.get('remark'))
    return response(message="Feedback revoked Success")