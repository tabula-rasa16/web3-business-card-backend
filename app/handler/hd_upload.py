# 处理图片以及视频的上传
from app import app
from app.common.tools import response, params_preprocess,generate_unique_id
from app.common.const import *

# import random
from flask import Blueprint, request, jsonify, send_from_directory, Response
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from eth_account.messages import encode_defunct
# from eth_account import Account
# import datetime

from app.handler.hd_base import require

from app.bpurl import upload_bp

import os
import uuid
from werkzeug.utils import secure_filename


# 配置上传路径
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
IMAGE_FOLDER = app.config['IMAGE_FOLDER']
VIDEO_FOLDER = app.config['VIDEO_FOLDER']


# 设置最大文件大小
MAX_CONTENT_LENGTH = app.config['MAX_CONTENT_LENGTH']

# 支持的文件格式
ALLOWED_IMAGE_EXTENSIONS = app.config['ALLOWED_IMAGE_EXTENSIONS']
ALLOWED_VIDEO_EXTENSIONS = app.config['ALLOWED_VIDEO_EXTENSIONS']

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, folder):
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(folder, unique_filename)
    file.save(file_path)
    return unique_filename, file_path

# 图片上传
@upload_bp.route('/image', methods=['POST'])
# @jwt_required()
def upload_image():
    if 'image' not in request.files:
        return response(code=400,message= 'No image part')
    file = request.files['image']
    if file.filename == '':
        return response(code=400,message= 'No selected image')
    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename, _ = save_file(file, IMAGE_FOLDER)
        return response(data={'filename': filename, 'url': f'{IMAGE_UPLOAD_PATH}/{filename}'},message= 'Image uploaded successfully')
        # return jsonify({'success': True, 'filename': filename, 'url': f'{path}'})
    else:
        return response(code=400,message= 'Invalid image format')
        # return jsonify({'success': False, 'message': 'Invalid image format'}), 400


# 图片批量上传
@upload_bp.route('/images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return response(code=400,message= 'No images part')

    files = request.files.getlist('images')  # 获取同名字段的多个文件
    if not files:
        return response(code=400,message= 'No images selected')

    uploaded = []

    for file in files:
        if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            filename, _ = save_file(file, IMAGE_FOLDER)
            uploaded.append({
                'filename': filename,
                'url': f'{IMAGE_UPLOAD_PATH}/{filename}'
            })

    if uploaded:
        return response(data={'uploaded': uploaded},message= 'Images uploaded successfully')
    else:
        return response(code=400,message= 'No valid images uploaded')


# 视频上传
@upload_bp.route('/video', methods=['POST'])
# @jwt_required()
def upload_video():
    if 'video' not in request.files:
        return response(code=400,message= 'No video part')
    file = request.files['video']
    if file.filename == '':
        return response(code=400,message= 'No selected video')
    if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        filename, _ = save_file(file, VIDEO_FOLDER)
        return response(data={'filename': filename, 'url': f'{VIDEO_UPLOAD_PATH}/{filename}'},message= 'Video uploaded successfully')
        # return jsonify({'success': True, 'filename': filename, 'url': f'/uploads/videos/{filename}'})
    else:
        return response(code=400,message= 'Invalid video format')



@app.route('/download/<path:fileurl>', methods=['GET','POST'])
def download_file(fileurl):
    """
    提供上传文件的访问
    """
    try:

        # 获取文件名部分
        filename = os.path.basename(fileurl)  # 3eaf939e398c4229bea453c09500a482.mkv

        # 获取路径部分
        rel_directory = os.path.dirname(fileurl)  # /uploads/videos
        # 构建正确的目录路径
        directory = os.path.join(app.config['PROJECT_ROOT'], rel_directory)
        # directory = os.path.dirname(app.config['PROJECT_ROOT'])
        
        
        # 打印调试信息
        print(f"访问文件: 目录={directory}, 文件={filename}")
        
        return send_from_directory(directory, filename, as_attachment=False)
    except Exception as e:
        print(f"错误: {str(e)}")
        return response(code=500,message= f"Error: {str(e)}")
    
# 流式下载
@app.route('/downloadStream/<filename>')
def stream_download_file(fileurl):
    def send_file():
        store_path = os.path.join(app.config['PROJECT_ROOT'], fileurl)
        with open(store_path, 'rb') as targetfile:
            while True:
                data = targetfile.read(1 * 1024 * 1024) # 每次读取1MB
                if not data:
                    break
        yield data
    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % fileurl
    return response




# @upload_bp.route('/<media_type>/<filename>')
# def uploaded_file(media_type, filename):
#     if media_type not in ['images', 'videos']:
#         return jsonify({'success': False, 'message': 'Invalid media type'}), 400
#     folder = os.path.join(UPLOAD_FOLDER, media_type)
#     return send_from_directory(folder, filename)