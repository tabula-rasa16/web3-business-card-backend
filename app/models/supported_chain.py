from app import mysql
from app.common.tools import datetime_serializer


# supported_chain表

def get_all_supported_chains():
    """查询所有支持的链"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM supported_chain WHERE data_status = 0")
    chains = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(chains is not None):
        for item in chains:
            temp = {
                "id": item[0],
                "key": item[1],
                "descrption": item[2],
                "data_status": item[3],
                "created_at": datetime_serializer(item[4]),
                "updated_at": datetime_serializer(item[5]),
            }
            result.append(temp.copy())
    return result

def get_supported_chains_by_id(chain_id):
    """通过 ID 查询单个支持的链"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM supported_chain WHERE id = %s AND data_status = 0", (chain_id,))
    item = cur.fetchone()
    cur.close()
    result = {
                "id": item[0],
                "key": item[1],
                "descrption": item[2],
                "data_status": item[3],
                "created_at": datetime_serializer(item[4]),
                "updated_at": datetime_serializer(item[5]),
            }
    return result
