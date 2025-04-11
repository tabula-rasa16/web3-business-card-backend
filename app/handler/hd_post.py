from flask import request, jsonify
from app import app
# import models.users as users_db
import app.models.posts as posts_db
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

from app.bpurl import post_bp


# 创建贴子
@post_bp.route('/create', methods=['POST'])
# @jwt_required()
@require("user_id","content")
def create_post():
    data = request.json
    data = params_preprocess(data)
    id = posts_db.add_post(data['user_id'], data['content'], data.get('media_url'))
    return response(data={"post_id": id}, message="Post created Success")


# 获取用户发布过的贴子列表
@post_bp.route('/list/', methods=['GET'])
# @jwt_required()
def get_post_list_by_user():
    user_id = request.args.get("user_id")
    post_list = posts_db.get_posts_by_user_id(user_id)
    for post in post_list:
        if post.get("media_url"):
            post["media_url"] = [url for url in post["media_url"].split(",")]
        else:
            post["media_url"] = []
    return response(data=post_list, message="Get post list success")


# 根据id获取单个贴子
@post_bp.route('/getRecord', methods=['GET'])
# @jwt_required()
def get_post_by_id():
    post_id = request.args.get("id")
    post_baseinfo = posts_db.get_post_by_id(post_id)
    if post_baseinfo.get("media_url"):
    # 对字符串以,分割
        post_baseinfo["media_url"] = [url for url in post_baseinfo["media_url"].split(",")]
    else:
        post_baseinfo["media_url"] = []
    # 获取一级评论列表
    comments = comments_db.get_comments_by_post_id(post_id)

    # 获取点赞信息
    likes = posts_db.get_likes_by_post_id(post_id)

    result= {
        "post":post_baseinfo,
        "comments":comments,
        "likes":likes
    }
    return response(data=result, message="Get post success")


# 删除贴子
@post_bp.route('/delete', methods=['POST'])
# @jwt_required()
@require("id")
def delete_post():
    data = request.json
    data = params_preprocess(data)
    posts_db.delete_post(data['id'])
    return response(message="Post delete Success")


# 获取朋友圈
@post_bp.route('/getMoments', methods=['POST'])
# @jwt_required()
@require("user_id", "page_num")
def get_moments():
    data = request.json
    data = params_preprocess(data)
    if data.get("page_size"):
        page_size = data.get("page_size")
    else:
        page_size = PAGE_SIZE
    post_list = posts_db.get_following_posts(data['user_id'], data['page_num'], page_size)
    for post in post_list:
        if post.get("media_url"):
            post["media_url"] = [url for url in post["media_url"].split(",")]
        else:
            post["media_url"] = []
    is_last_page = True if len(post_list) < page_size else False
    result = {
        "moments": post_list,
        "current_page": data['page_num'],
        "page_size": page_size,
        "is_last_page": is_last_page
    }
    return response(data=result, message="Get moments success")


# 点赞贴子
@post_bp.route('/like', methods=['POST'])
# @jwt_required()
@require("user_id", "post_id")
def like_post():
    data = request.json
    data = params_preprocess(data)
    # 先检查是否点过赞
    if posts_db.check_like(data['user_id'], data['post_id']):
        return response(message="Already liked", code=400)

    posts_db.add_like(data['user_id'], data['post_id'])
    return response(message="Like post success")


# 取消点赞贴子
@post_bp.route('/unlike', methods=['POST'])
# @jwt_required()
@require("user_id", "post_id")
def unlike_post():
    data = request.json
    data = params_preprocess(data)
    # 先检查是否点过赞
    if not posts_db.check_like(data['user_id'], data['post_id']):
        return response(message="Not liked", code=400)
    
    posts_db.delete_like(data['user_id'], data['post_id'])
    return response(message="Unlike post success")


# 获取曾赞过的贴子列表
@post_bp.route('/getLikedPosts', methods=['GET'])
# @jwt_required()
def get_liked_posts():
    user_id = request.args.get("user_id")
    post_list = posts_db.get_likes_by_user_id(user_id)
    for post in post_list:
        if post.get("media_url"):
            post["media_url"] = [url for url in post["media_url"].split(",")]
        else:
            post["media_url"] = []
    return response(data=post_list, message="Get liked posts success")


