from flask import request, jsonify
from app import app
# import models.users as users_db
import app.models.comments as comments_db
from app.common.tools import response, params_preprocess,generate_unique_id
from app.common.const import *

# import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import comment_bp


# 创建评论
@comment_bp.route('/create', methods=['POST'])
# @jwt_required()
@require("user_id", "post_id", "content")
def create_comment():
    data = request.json
    data = params_preprocess(data)
    parent_id = data.get("parent_id") if data.get("parent_id") else 0
    result = comments_db.add_comment(data['user_id'], data['post_id'], data['content'], parent_id)

    return response(data={"comment_id":result}, message="Comment created Success")


# 获取用户发布过的评论列表
@comment_bp.route('/list/', methods=['GET'])
# @jwt_required()
def get_comment_list_by_user():
    user_id = request.args.get("user_id")
    comment_list = comments_db.get_comments_by_user_id(user_id)
    return response(data=comment_list, message="Get comment list success")


# 根据评论id获取其子评论
@comment_bp.route('/getChildren', methods=['GET'])
# @jwt_required()
def get_children_commments_by_id():
    comment_id = request.args.get("id")
    children_comments = comments_db.get_replys_by_parent_id(comment_id)
    return response(data=children_comments, message="Get children comments success")


# 删除评论（级联删除）
@comment_bp.route('/delete', methods=['POST'])
# @jwt_required()
@require("id")
def delete_comment():
    data = request.json
    data = params_preprocess(data)
    comments_db.delete_comment(data['id'])
    return response(message="Comment delete Success")


