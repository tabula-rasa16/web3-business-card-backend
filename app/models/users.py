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
    result = {
        "id": user[0]
    }
    return result

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s and data_status=0", (user_id,))
    user = cur.fetchone()
    cur.close()
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

def add_user(wallet_address, username, avatar_url, gender, bio):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (wallet_address, username, avatar_url, gender, bio) VALUES (%s, %s, %s, %s, %s)",
                (wallet_address, username, avatar_url, gender, bio))
    mysql.connection.commit()
    cur.close()

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
