from app import mysql
from app.common.tools import datetime_serializer

def get_comments_by_post_id(post_id):
    """根据贴子 ID 获取其所有一级评论"""
    cur = mysql.connection.cursor()
    sql = '''SELECT c.id , c.user_id , u.username , u.avatar_url, c.content , c.created_at FROM comments c
            LEFT JOIN users u ON c.user_id = u.id 
            WHERE c.post_id = %s AND c.data_status=0 AND u.data_status=0 AND c.parent_id=0 order by c.created_at desc'''
    cur.execute(sql, (post_id,))
    comments = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(comments is not None):
        for item in comments:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "user_name": item[2],
                "avatar_url": item[3],
                "content": item[4],
                "created_at": datetime_serializer(item[5]),
            }
            result.append(temp.copy())
    return result


def get_comments_by_user_id(post_id):
    """根据用户 ID 获取其发布过的评论"""
    cur = mysql.connection.cursor()
    sql = '''SELECT c.id , c.user_id , u.username , u.avatar_url, c.content , c.created_at, p.id as post_id, p.content as post_content FROM comments c
            LEFT JOIN posts p ON c.post_id = p.id 
            LEFT JOIN users u ON p.user_id = u.id 
            WHERE c.user_id = %s AND c.data_status=0 AND p.data_status=0 AND u.data_status=0
            order by c.created_at desc'''
    cur.execute(sql, (post_id,))
    comments = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(comments is not None):
        for item in comments:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "user_name": item[2],
                "avatar_url": item[3],
                "content": item[4],
                "created_at": datetime_serializer(item[5]),
                "post_id": item[6],
                "post_content": item[7]
            }
            result.append(temp.copy())
    return result

def get_replys_by_parent_id(parent_id):
    """通过父评论 ID 获取其所有子回复"""
    cur = mysql.connection.cursor()
    sql = '''SELECT c.id , c.user_id , u.username , u.avatar_url, c.content , c.created_at FROM comments c
            LEFT JOIN users u ON c.user_id = u.id 
            WHERE c.parent_id = %s AND c.data_status=0 AND u.data_status=0 order by c.created_at desc'''
    cur.execute(sql, (parent_id,))
    comments = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(comments is not None):
        for item in comments:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "user_name": item[2],
                "avatar_url": item[3],
                "content": item[4],
                "created_at": datetime_serializer(item[5]),
            }
            result.append(temp.copy())
    return result

def add_comment(user_id, post_id, content, parent_id=0):
    """添加新的评论"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO comments (user_id, post_id, content, parent_id)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (user_id, post_id, content, parent_id))
        mysql.connection.commit()
        cur.close()
        return cur.lastrowid  
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}


def delete_comment(comment_id):
    """删除评论"""
    cur = mysql.connection.cursor()
    try:
        # 级联删除，删除评论及其下所有层级的子评论
        sql = '''
                WITH RECURSIVE comment_tree AS (
                    SELECT id 
                    FROM comments 
                    WHERE id = %s
                    
                    UNION ALL
                    
                    SELECT c.id 
                    FROM comments c
                    JOIN comment_tree ct ON c.parent_id = ct.id
                )
                UPDATE comments 
                SET data_status = 1
                WHERE id IN (SELECT id FROM comment_tree);'''
        
        cur.execute(sql, (comment_id,))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功删除
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}
