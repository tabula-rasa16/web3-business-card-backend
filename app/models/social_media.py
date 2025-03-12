from app import mysql
from app.common.tools import datetime_serializer

# t_social_media表

def get_all_social_media():
    """查询所有有效的社交媒体"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_social_media WHERE data_status = 0")
    social_media = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(social_media is not None):
        for item in social_media:
            temp = {
                "id": item[0],
                "app_name": item[1],
                "app_type": item[2],
                "app_key": item[3],
                "style": item[4],
                "data_status": item[5],
                "remark": item[6],
                "creator": item[7],
                "created_at": datetime_serializer(item[8]),
            }
            result.append(temp.copy())
    return result

def get_social_media_by_id(media_id):
    """通过 ID 查询单个社交媒体"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_social_media WHERE id = %s AND data_status = 0", (media_id,))
    item = cur.fetchone()
    cur.close()
    result = {
                "id": item[0],
                "app_name": item[1],
                "app_type": item[2],
                "app_key": item[3],
                "style": item[4],
                "data_status": item[5],
                "remark": item[6],
                "creator": item[7],
                "created_at": datetime_serializer(item[8]),
            }
    return result
