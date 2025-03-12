from flask import request, jsonify
from app import app
# import models.users as users_db
import app.models.business_card as business_card_db
import app.models.social_media as social_media_db
from app.common.tools import response, params_preprocess

# import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import businessCard_bp


# 获取系统内支持的社交平台列表（用于动态表单）
@businessCard_bp.route('/getSocialMedia', methods=['GET'])
def get_social_media_list():
    list = social_media_db.get_all_social_media()
    if not list:
        return response(code=404, message="Social Media list is not found")
    return response(data=list)

# 获取名片信息
@businessCard_bp.route('/getcard/', methods=['GET'])
# @jwt_required()
def get_businessCard():
    user_id = request.args.get("user_id")
    business_card_base_info = business_card_db.get_business_cards_by_user_id(user_id)
    if not business_card_base_info:
        return response(code=404, message="Business card is not found")
    social_accounts = business_card_db.get_social_accounts_by_user_id(user_id)
    result = {"business_card_base_info":business_card_base_info,
              "social_accounts":social_accounts}
    return response(data=result)


# 创建名片
@businessCard_bp.route('/create', methods=['POST'])
# @jwt_required()
@require("user_id","display_name","debox_account")
def create_businessCard():
    data = request.get_json()
    data = params_preprocess(data)
    social_account_list = data['social_account_list']
    # 创建名片个人基本信息部分
    business_card_db.add_business_card(data['user_id'], data['display_name'], data['company'], data['job_title'], data['website_url'], data['portfolio_url'], data['debox_account'], data['email'], data['phone'])
    # 创建名片社交平台部分
    if social_account_list:
        insert_list = []
        for item in social_account_list:
            t = (data['user_id'],item['platform'], item['account_handle'], item['profile_url'])
            insert_list.append(t)
        business_card_db.batch_add_social_accounts(insert_list)
    # todo 创建数字资产信息部分
    return response(message="Create business card successfully")



# 修改名片信息
@businessCard_bp.route('/update', methods=['POST'])
# @jwt_required()
@require("id","user_id","display_name","debox_account")
def update_businessCard():
    data = request.get_json()
    data = params_preprocess(data)
    # 账户列表
    social_account_list = data['social_account_list']
    # 更新名片个人基本信息部分
    business_card_db.update_business_card(data['id'], data['display_name'], data['company'], data['job_title'], data['website_url'], data['portfolio_url'], data['debox_account'], data['email'], data['phone'])
    # 更新名片社交平台部分
    if social_account_list:
        # 先删除之前的记录
        business_card_db.batch_delete_social_accounts(data["user_id"])
        # 再插入新的记录
        insert_list = []
        for item in social_account_list:
            t = (data['user_id'],item['platform'], item['account_handle'], item['profile_url'])
            insert_list.append(t)
        business_card_db.batch_add_social_accounts(insert_list)
    # todo 更新数字资产信息部分
    return response(message="Update business card successfully")

    

