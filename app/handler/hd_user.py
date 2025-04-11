from flask import request, jsonify
from app import app
import app.models.users as users_db
# import models.business_card as business_card_db
from app.common.tools import response,params_preprocess
from app.common.const import *

# import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import user_bp







# 获取所有用户
@user_bp.route('/getAll', methods=['GET'])
def get_all_users():

    users = users_db.get_users()
    return response(data=users)

# 根据用户钱包地址获取其用户id
@user_bp.route('/getIdByAddress', methods=['POST'])
# @jwt_required()
@require("wallet_address")
def get_user_id_by_wallet_address():
    data = request.json
    data = params_preprocess(data)
    result = users_db.get_user_id_by_wallet_address(data['wallet_address'])
    
    return response(data=result)

# 获取用户基础信息（不包括数字资产）
@user_bp.route('/baseinfo/', methods=['GET'])
# @jwt_required()  # 需要携带 JWT Token
def get_user():
    """获取用户信息"""
    user_id = request.args.get("user_id")
    # current_user_address = get_jwt_identity()  # 获取 JWT 解析出的钱包地址

    if not user_id:
        return response(code=400, message="User ID is required")
    
    user = users_db.get_user_by_id(user_id)
    if not user:
        return response(code=404, message="User not found")

    return response(data=user)

# 创建用户
@user_bp.route('/create', methods=['POST'])
# @jwt_required()  # 需要携带 JWT Token
@require("wallet_address", "username")
def create_user():
    data = request.json
    data = params_preprocess(data)
    print(data)
    # if not data or 'wallet_address' not in data or 'username' not in data:
    #         return response(code=400, message="Missing required fields")
    user_id = users_db.add_user(data['wallet_address'], data['username'], data.get('avatar_url'), data.get('gender'), data.get('bio'))
    return response(code=200, message="User created Success",data = {"user_id": user_id})

@user_bp.route('/update', methods=['POST'])
# @jwt_required()  # 需要携带 JWT Token
@require("user_id", "username")
def update_user():
    data = request.json
    data = params_preprocess(data)
    users_db.update_user(data['user_id'], data['username'], data.get('avatar_url'), data.get('gender'), data.get('bio'))
    return response(code=200, message="User updated Success")

@user_bp.route('/delete', methods=['POST'])
# @jwt_required()  # 需要携带 JWT Token
@require("user_id")
def delete_user():
    data = request.json
    data = params_preprocess(data)
    users_db.delete_user(data['user_id'])
    return response(code=200, message="User deleted Success")



# 用户关注相关
# 获取用户的关注列表
@user_bp.route('/getFollowings', methods=['GET'])
# @jwt_required()
def get_followings():
    user_id = request.args.get("user_id")

    if not user_id:
        return response(code=400, message="User ID is required")
    
    followings = users_db.get_followings_by_follower_id(user_id)
    return response(data=followings,message="Get User followings Success")

# 获取用户的粉丝列表
@user_bp.route('/getFollowers', methods=['GET'])
# @jwt_required()
def get_followers():
    user_id = request.args.get("user_id")
    if not user_id:
        return response(code=400, message="User ID is required")

    followers = users_db.get_followers_by_following_id(user_id)
    return response(data=followers, message="Get User followers Success")

# 关注用户
@user_bp.route('/follow', methods=['POST'])
# @jwt_required()
@require("follower_id", "following_id")
def follow_user():
    data = request.json
    data = params_preprocess(data)

    # 检查之前是否已关注过
    if users_db.get_follow_by_two_ids(data['follower_id'], data['following_id']):
        return response(code=400, message="Already followed")
    # 添加关注关系
    users_db.add_follow(data['follower_id'], data['following_id'])
    return response(code=200, message="Follow user Success")

# 取消关注用户
@user_bp.route('/unfollow', methods=['POST'])
# @jwt_required()
@require("follower_id", "following_id")
def unfollow_user():
    data = request.json
    data = params_preprocess(data)
    users_db.delete_follow(data['follower_id'], data['following_id'])
    return response(code=200, message="Unfollow user Success")

# 获取两个用户之间的关注关系（用于前端展示“已关注”/“未关注”/“已互粉”/“回关”等）
@user_bp.route('/followRelation', methods=['POST'])
# @jwt_required()
@require("subject_id", "object_id")
def get_follow_relation():
    data = request.json
    data = params_preprocess(data)
    subject_follow_object = users_db.get_follow_by_two_ids(data['subject_id'], data['object_id']) #主体是否关注客体
    object_follow_subject = users_db.get_follow_by_two_ids(data['object_id'], data['subject_id']) #客体是否关注主体

    if subject_follow_object and object_follow_subject:
        follow_relation = USER_FOLLOW_STATUS_MUTUAL
    elif subject_follow_object:
        follow_relation = USER_FOLLOW_STATUS_FOLLOWED
    elif object_follow_subject:
        follow_relation = USER_FOLLOW_STATUS_FOLLOWBACK
    else:
        follow_relation = USER_FOLLOW_STATUS_UNFOLLOWED
    
    result = {
        "follow_relation": follow_relation
    }

    return response(data=result, message="Get follow relation Success")