from app import mysql
from app.common.tools import datetime_serializer


# Users表
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE data_status=0")
    users = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(users is not None):
        for item in users:
            temp = {
                "id": item[0],
                "wallet_address": item[1],
                "username": item[2],
                "avatar_url": item[3],
                "gender": item[4],
                "bio": item[5],
                "data_status": item[6],
                "created_at": datetime_serializer(item[7]),
                "updated_at": datetime_serializer(item[8])
            }
            result.append(temp.copy())
        # print("result:", result)
    return result

def get_user_id_by_wallet_address(wallet_address):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE wallet_address = %s and data_status=0", (wallet_address,))
    user = cur.fetchone()
    cur.close()
    if user is not None:
        result = {
            "id": user[0]
        }
        return result
    return None

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s and data_status=0", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user is not None:
        result = {
            "id": user[0],
            "wallet_address": user[1],
            "username": user[2],
            "avatar_url": user[3],
            "gender": user[4],
            "bio": user[5],
            "data_status": user[6],
            "created_at": datetime_serializer(user[7]),
            "updated_at": datetime_serializer(user[8])
        }
        return result
    return None

def add_user(wallet_address, username, avatar_url, gender, bio):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (wallet_address, username, avatar_url, gender, bio) VALUES (%s, %s, %s, %s, %s)",
                (wallet_address, username, avatar_url, gender, bio))
    mysql.connection.commit()
    cur.close()
    return cur.lastrowid  

def update_user(user_id, username, avatar_url, gender, bio):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET username=%s, avatar_url=%s, gender=%s, bio=%s, updated_at=NOW() WHERE id=%s",
                (username, avatar_url, gender, bio, user_id))
    mysql.connection.commit()
    cur.close()

def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET data_status=1 WHERE id=%s", (user_id,))
    mysql.connection.commit()
    cur.close()

# Follows表
def get_followings_by_follower_id(user_id):
    '''获取此用户关注的人'''
    cur = mysql.connection.cursor()
    cur.execute('''SELECT f.id, f.following_id , f.created_at , u.username , u.avatar_url ,u.bio  FROM follows f
                left join users u on f.following_id = u.id 
                WHERE f.follower_id = %s and f.data_status=0 and u.data_status=0''', (user_id,))
    follows = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(follows is not None):
        for item in follows:
            temp = {
                "id": item[0],
                "following_id": item[1],
                "created_at": datetime_serializer(item[2]),
                "username": item[3],
                "avatar_url": item[4],
                "bio": item[5]
            }
            result.append(temp.copy())
    return result

def get_followers_by_following_id(user_id):
    '''获取关注此用户的人'''
    cur = mysql.connection.cursor()
    cur.execute('''SELECT f.id, f.follower_id , f.created_at , u.username , u.avatar_url ,u.bio  FROM follows f
                left join users u on f.follower_id = u.id 
                WHERE f.following_id = %s and f.data_status=0 and u.data_status=0''', (user_id,))
    follows = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(follows is not None):
        for item in follows:
            temp = {
                "id": item[0],
                "follower_id": item[1], 
                "created_at": datetime_serializer(item[2]),
                "username": item[3],
                "avatar_url": item[4],
                "bio": item[5]
            }
            result.append(temp.copy())
    return result

def get_follow_by_two_ids(follower_id, following_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM follows WHERE follower_id = %s and following_id = %s and data_status=0", (follower_id, following_id))
    follow = cur.fetchone()
    cur.close()
    if follow is not None:
        result = {
            "id": follow[0],
            "follower_id": follow[1],
            "following_id": follow[2],
            "created_at": datetime_serializer(follow[3]),
            "data_status": follow[4],
            "is_followed": True
        }
        return result
    return None

def add_follow(follower_id, following_id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)",
                (follower_id, following_id))
    mysql.connection.commit()
    cur.close()
    return cur.lastrowid

def batch_add_follow(follower_id,follow_list):
    if not follow_list or not follower_id or len(follow_list) == 0:
        return False

    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)
        """
        values = [(follower_id, item) for item in follow_list]

        cur.executemany(sql, values)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)} 

def delete_follow(follower_id, following_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE follows SET data_status=1 WHERE follower_id=%s and following_id=%s", (follower_id, following_id))
    mysql.connection.commit()