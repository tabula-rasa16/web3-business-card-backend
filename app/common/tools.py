from flask import jsonify
from datetime import datetime

# 返回数据格式模板
def response(code=200, data=None, message="Success"):
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code


# 参数预处理
def params_preprocess(params):
    processed_data = {}
    for key, value in params.items():
        if value == "":
            processed_data[key] = None
        else:
            processed_data[key] = value
    return processed_data


# 将datetime类型的数据转换为字符串，以便后续json格式化
def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
