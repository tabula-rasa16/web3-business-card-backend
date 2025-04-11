from app import mysql
from app.common.tools import datetime_serializer

# posts表
def get_posts_by_user_id(user_id):
    """根据用户 ID 获取其发布过的所有贴子"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE user_id = %s AND data_status=0 order by created_at desc", (user_id,))
    posts = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(posts is not None):
        for item in posts:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "content": item[2],
                "media_url": item[3],
                "data_status": item[4],
                "created_at": datetime_serializer(item[5]),
                "updated_at": datetime_serializer(item[6])
            }
            result.append(temp.copy())
    return result

def get_post_by_id(post_id):
    """通过 ID 获取单个贴子"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s AND data_status=0", (post_id,))
    item = cur.fetchone()
    cur.close()
    if item is None:
        return None
    result = {
                "id": item[0],
                "user_id": item[1],
                "content": item[2],
                "media_url": item[3],
                "data_status": item[4],
                "created_at": datetime_serializer(item[5]),
                "updated_at": datetime_serializer(item[6])
            }
    return result

def add_post(user_id, content, media_url=None):
    """添加新的贴子"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO posts (user_id, content, media_url)
            VALUES (%s, %s, %s)
        """
        cur.execute(sql, (user_id, content, media_url))
        mysql.connection.commit()
        cur.close()
        return cur.lastrowid  
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}
    
def delete_post(post_id):
    """删除贴子"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            UPDATE posts SET data_status = 1 WHERE id = %s
        """
        cur.execute(sql, (post_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()

def get_following_posts(user_id, page_num, page_size):
    """获取关注用户发布的贴子(朋友圈)，支持分页"""
    cur = mysql.connection.cursor()

    offset = (page_num - 1) * page_size
    sql = '''
        SELECT * FROM posts 
        WHERE user_id IN (SELECT following_id FROM follows WHERE follower_id = %s AND data_status=0) 
        AND data_status=0 
        order by created_at desc 
        limit %s offset %s
    '''
    cur.execute(sql, (user_id,page_size, offset))
    posts = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(posts is not None):
        for item in posts:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "content": item[2],
                "media_url": item[3],
                "data_status": item[4],
                "created_at": datetime_serializer(item[5]),
                "updated_at": datetime_serializer(item[6])
            }
            result.append(temp.copy())
    return result



# likes表，处理贴子点赞
def get_likes_by_post_id(post_id):
    """根据贴子 ID 获取其点赞过的所有用户"""
    cur = mysql.connection.cursor()
    sql = '''
            SELECT l.id , l.user_id , u.username , l.created_at  FROM likes l
            left join users u on l.user_id = u.id 
            WHERE l.post_id = %s and l.data_status=0 and u.data_status=0
            order by l.created_at desc '''
    cur.execute(sql, (post_id,))
    likes = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(likes is not None):
        for item in likes:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "username": item[2],
                "created_at": datetime_serializer(item[3])
            }
            result.append(temp.copy())
    return result


def get_likes_by_user_id(user_id):
    """根据用户 ID 获取其点赞过的所有贴子"""
    cur = mysql.connection.cursor()
    sql='''
        SELECT l.id , l.post_id , l.created_at , p.user_id , u.username , u.avatar_url , p.content , p.media_url  FROM likes l
        left join posts p on l.post_id = p.id 
        left join users u on p.user_id = u.id 
        WHERE l.user_id = %s AND u.data_status=0 and p.data_status=0 and l.data_status=0
        order by l.created_at desc'''
    
    cur.execute(sql, (user_id,))
    likes = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(likes is not None):
        for item in likes:
            temp = {
                "id": item[0],
                "post_id": item[1],
                "created_at": datetime_serializer(item[2]),
                "user_id": item[3],
                "username": item[4],
                "avatar_url": item[5],
                "content": item[6],
                "media_url": item[7]
            }
            result.append(temp.copy())
    return result


def check_like(user_id, post_id):
    """检查用户是否点赞过该贴子"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id = %s AND post_id = %s AND data_status=0", (user_id, post_id))
    item = cur.fetchone()
    cur.close()
    if item is None:
        return None
    result = {
            "id": item[0]
    }
    return result

def add_like(user_id, post_id):
    """添加点赞"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO likes (user_id, post_id)
            VALUES (%s, %s)
        """
        cur.execute(sql, (user_id, post_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}
    
def delete_like(user_id, post_id):
    """删除点赞"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            UPDATE likes SET data_status = 1 WHERE user_id = %s AND post_id = %s
        """
        cur.execute(sql, (user_id, post_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
