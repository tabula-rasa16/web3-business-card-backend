from app import mysql
from app.common.tools import datetime_serializer

def get_collected_cards_by_user_id(owner_id):
    """获取用户收藏的所有名片"""
    cur = mysql.connection.cursor()
    sql = """
        SELECT bc.id, bc.display_name, bc.debox_account, bc.phone, bc.company, u.avatar_url, bc.share_token, cc.added_at, bc.shared_status  
        FROM card_collection cc
        left join business_cards bc
        on cc.card_id = bc.id
        left join users u
        on bc.user_id = u.id 
        WHERE cc.owner_id = %s and cc.data_status=0 and bc.data_status=0 and u.data_status=0
        order by cc.added_at desc
    """
    cur.execute(sql, (owner_id,))
    cards = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(cards is not None):
        for item in cards:
            temp = {
                "id": item[0],
                "display_name": item[1],
                "debox_account": item[2],
                "phone": item[3],
                "company": item[4],
                "avatar_url": item[5],
                "share_token": item[6],
                "added_at": datetime_serializer(item[7]),
                "shared_status": item[8]
            }
            result.append(temp.copy())
    return result

def get_collection_entry(owner_id, card_id):
    """根据用户 ID 和名片 ID 查询是否已收藏"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM card_collection WHERE owner_id = %s AND card_id = %s AND data_status=0", 
                (owner_id, card_id))
    item = cur.fetchone()
    cur.close()
    if item is not None:
        result = {
            "id": item[0],
            "owner_id": item[1],
            "card_id": item[2],
            "added_at": item[3]
        }
        return result
    return None

def add_card_to_collection(owner_id, card_id):
    """添加名片到收藏夹"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO card_collection (owner_id, card_id)
            VALUES (%s, %s)
        """
        cur.execute(sql, (owner_id, card_id))
        mysql.connection.commit()
        cur.close()
        return cur.lastrowid  # 返回插入的收藏记录 ID
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}

def batch_add_cards_to_collection(collection_list):
    """批量添加名片到收藏夹"""
    if not collection_list:
        return False

    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO card_collection (owner_id, card_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE data_status=0
        """
        values = [(entry["owner_id"], entry["card_id"]) for entry in collection_list]

        cur.executemany(sql, values)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}  # 批量收藏失败

def remove_card_from_collection(owner_id, card_id):
    """移除收藏的名片"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE card_collection SET data_status=1 WHERE owner_id = %s AND card_id = %s", (owner_id, card_id))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功删除
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}

def batch_remove_cards_from_collection(collection_list):
    """批量移除收藏的名片"""
    if not collection_list:
        return False

    cur = mysql.connection.cursor()
    try:
        sql = "UPDATE card_collection SET data_status=1 WHERE owner_id = %s AND card_id = %s"
        values = [(entry["owner_id"], entry["card_id"]) for entry in collection_list]

        cur.executemany(sql, values)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}  # 批量删除失败