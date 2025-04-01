from flask import request, jsonify
from app import app
# import models.users as users_db
import app.models.digital_assets as digital_assets_db
import app.models.users as users_db
import app.models.supported_chain as supported_chain_db
from app.common.tools import response, params_preprocess,generate_unique_id
from app.common.moralis_api import *

# import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import digitalAsset_bp

import json
import requests


# 获取Moralis API支持的链
@digitalAsset_bp.route('/getSupportedChains', methods=['GET'])
# @jwt_required
def get_supported_chains():
    result = supported_chain_db.get_all_supported_chains()
    return response(data=result)


# 通过Moralis API获取钱包中的token
@digitalAsset_bp.route('/getWalletTokens', methods=['POST'])
# @jwt_required
@require("address","chain")
def get_wallet_tokens():
    data = request.json
    data = params_preprocess(data)
    token_addresses = data["token_addresses"] if data.get("token_addresses") else []
    result = get_token_balance(data["address"], data["chain"], token_addresses, data.get("limit"))
    return response(data=result)


    # headers = {"x-api-key": app.config["MORALIS_API_KEY"]}
    # url = f"https://deep-index.moralis.io/api/v2/{address}/erc20?chain={chain}"
    
    # response = requests.get(url, headers=headers)
    # return jsonify(response.json())

# 通过Moralis API获取钱包中的nft
@digitalAsset_bp.route('/getWalletNfts', methods=['POST'])
# @jwt_required
@require("address","chain")
def get_nfts():
    data = request.json
    data = params_preprocess(data)
    token_addresses = data["token_addresses"] if data.get("token_addresses") else []
    result = get_wallet_nfts(wallet_address=data["address"], chain=data["chain"], token_addresses=token_addresses, limit=data.get("limit"))
    return response(data=result)



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
# @digitalAsset_bp.route('/get/', methods=['GET'])
# # @jwt_required
# def get_digital_asset():
#     user_id = request.args.get("user_id")
#     is_display = request.args.get("is_display")
#     # 获取数字资产记录
#     if is_display is not None:
#         digital_assets = digital_assets_db.get_assets_by_user_id(user_id, is_display)
#     else:
#         digital_assets = digital_assets_db.get_assets_by_user_id(user_id)
#     return response(data=digital_assets, message="Get digital asset successfully")


# 根据用户id获取数字资产记录
@digitalAsset_bp.route('/get/', methods=['GET'])
# @jwt_required
def get_digital_asset():
    user_id= request.args.get("user_id")
    chain = request.args.get("chain")
    limit = request.args.get("limit")


    if limit is not None:
        try:
            limit = int(limit)  
        except ValueError:
            # 转换失败，返回错误信息
            return response(code=400, message="Invalid limit parameter, must be a number")

    # 获取数字资产记录
    # 根据用户id获取钱包地址
    user_wallet_address = users_db.get_user_by_id(user_id).get("wallet_address").lower()

    # 从库中查询其资产信息，分别查token和nft
    token_addresses = []
    nft_addresses = []
    if user_wallet_address is not None and user_wallet_address != "":
        digital_assets = digital_assets_db.get_assets_by_user_id(user_id)
        for item in digital_assets:
            if item.get("asset_type") == 'TOKEN':
                token_addresses.append(item.get("contract_address").lower())
            elif item.get("asset_type") == 'NFT':
                nft_addresses.append(item.get("contract_address").lower())
   
    
    # 从对应的链上获取token和nft信息
    token_list = get_token_balance(wallet_address=user_wallet_address, chain=chain, token_addresses=token_addresses, limit=limit)
   
    nft_list = get_wallet_nfts(wallet_address=user_wallet_address, chain=chain, limit=limit, token_addresses=nft_addresses)

    # 合并token和nft信息并返回
    result = {
        "token_list": token_list,
        "nft_list": nft_list
    }
    
    return response(data=result, message="Get digital asset successfully")





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


    
    

