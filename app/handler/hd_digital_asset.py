from flask import request, jsonify
from app import app
# import models.users as users_db
import app.models.digital_assets as digital_assets_db
from app.common.tools import response, params_preprocess,generate_unique_id

# import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import digitalAsset_bp

import json




# 在库中创建数字资产记录
@digitalAsset_bp.route('/create', methods=['POST'])
# @jwt_required
@require("user_id","asset_type","contract_address")
def create_digital_asset():
    data = request.json
    data = params_preprocess(data)
    # 对json对象进行处理
    if data.get("asset_metadata"):
        data["asset_metadata"] = json.dumps(data["asset_metadata"])
    # 创建数字资产记录
    result = digital_assets_db.add_digital_asset(data["user_id"],data["asset_type"],data["contract_address"],data.get("name"),data.get("token_id"),data.get("amount"),data.get("asset_metadata"),data.get("is_display"),data.get("display_order"))
    return response(message="Create digital asset successfully")

# 批量创建数字资产记录
@digitalAsset_bp.route('/batchCreate', methods=['POST'])
# @jwt_required
@require("asset_list")
def batch_create_digital_asset():
    data = request.json
    # data = params_preprocess(data)
    if not isinstance(data["asset_list"], list):
        return response(code=400, message="asset_list must be a list")
    else:
        for asset in data["asset_list"]:
            # 检测每个对象中都是否包含必填字段
            if not all(key in asset for key in ["user_id", "asset_type", "contract_address"]):
                return response(code=400, message="asset list item must contain user_id, asset_type, contract_address")
            # 对json对象进行处理
            if asset.get("asset_metadata"):
                asset["asset_metadata"] = json.dumps(asset["asset_metadata"])
        # 批量创建数字资产记录
        result = digital_assets_db.batch_insert_digital_assets(data["asset_list"])
        print(result)
        return response(message="Batch create digital asset successfully")
    
# 根据用户id获取数字资产记录(支持选择展示全部/展示已上架)
@digitalAsset_bp.route('/get/', methods=['GET'])
# @jwt_required
def get_digital_asset():
    user_id = request.args.get("user_id")
    is_display = request.args.get("is_display")
    # 获取数字资产记录
    if is_display is not None:
        digital_assets = digital_assets_db.get_assets_by_user_id(user_id, is_display)
    else:
        digital_assets = digital_assets_db.get_assets_by_user_id(user_id)
    return response(data=digital_assets, message="Get digital asset successfully")

# 批量更新数字资产记录
@digitalAsset_bp.route('/batchUpdate', methods=['POST'])
# @jwt_required
@require("asset_list")
def batch_update_digital_asset():
    data = request.json
    # data = params_preprocess(data)
    if not isinstance(data["asset_list"], list):
        return response(code=400, message="asset_list must be a list")
    else:
        for asset in data["asset_list"]:
            # 检测每个对象中都是否包含必填字段
            if not all(key in asset for key in ["user_id", "asset_type", "contract_address"]):
                return response(code=400, message="asset list item must contain user_id, asset_type, contract_address")
            # 对json对象进行处理
            if asset.get("asset_metadata"):
                asset["asset_metadata"] = json.dumps(asset["asset_metadata"])
        # 先删除之前的记录
        user_id = data["asset_list"][0]["user_id"]
        digital_assets_db.delete_digital_asset_by_user_id(user_id)
        # 批量插入新的数字资产记录
        digital_assets_db.batch_insert_digital_assets(data["asset_list"])
        return response(message="Batch update digital asset successfully")

# 删除某用户的全部数字资产记录
@digitalAsset_bp.route('/delete', methods=['POST'])
# @jwt_required
@require("user_id")
def delete_digital_asset():
    data = request.json
    data = params_preprocess(data)
    user_id = data["user_id"]
    # 删除数字资产记录
    digital_assets_db.delete_digital_asset_by_user_id(user_id)
    return response(message="Delete digital asset successfully")


    
    

