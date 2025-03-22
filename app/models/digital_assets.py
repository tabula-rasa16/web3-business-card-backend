from app import mysql
from app.common.tools import datetime_serializer


def get_assets_by_user_id(user_id, is_display=None):
    """根据用户 ID 获取其所有数字资产, 参数is_display为1时只获取要展示的资产"""
    
    cur = mysql.connection.cursor() 
    if is_display is None:
        cur.execute("SELECT * FROM digital_assets WHERE user_id = %s AND data_status=0", (user_id,))
    else:
        cur.execute("SELECT * FROM digital_assets WHERE user_id = %s AND is_display = %s AND data_status=0 order by display_order desc", (user_id, is_display))

    
    assets = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(assets is not None):
        for item in assets:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "asset_type": item[2],
                "name": item[3],
                "contract_address": item[4],
                "token_id": item[5],
                "amount": item[6],
                "asset_metadata": item[7],
                "is_display": item[8],
                "display_order": item[9],
                "created_at": datetime_serializer(item[10])
            }
            result.append(temp.copy())
    return result

def get_asset_by_id(asset_id):
    """通过 ID 获取单个数字资产"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM digital_assets WHERE id = %s AND data_status=0", (asset_id,))
    item = cur.fetchone()
    cur.close()
    if item is None:
        return None
    result = {
                "id": item[0],
                "user_id": item[1],
                "asset_type": item[2],
                "name": item[3],
                "contract_address": item[4],
                "token_id": item[5],
                "amount": item[6],
                "asset_metadata": item[7],
                "is_display": item[8],
                "display_order": item[9],
                "created_at": datetime_serializer(item[10])
            }
    return result

def add_digital_asset(user_id, asset_type, contract_address, name=None, token_id=None, amount=None, asset_metadata=None, is_display=None, display_order=None):
    """添加新的数字资产"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO digital_assets (user_id, asset_type, contract_address, name, token_id, amount, asset_metadata, is_display, display_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (user_id, asset_type, contract_address, name, token_id, amount, asset_metadata, is_display, display_order))
        mysql.connection.commit()
        cur.close()
        return cur.lastrowid  # 返回插入的资产 ID
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)} 


def update_digital_asset(asset_id, asset_type=None, contract_address=None, name=None, token_id=None, amount=None, asset_metadata=None, is_display=None, display_order=None):
    """更新数字资产信息（可选参数为 None 时不更新）"""
    cur = mysql.connection.cursor()
    update_fields = []
    values = []

    if asset_type:
        update_fields.append("asset_type=%s")
        values.append(asset_type)
    if contract_address:
        update_fields.append("contract_address=%s")
        values.append(contract_address)
    if name:
        update_fields.append("name=%s")
        values.append(name)
    if token_id:
        update_fields.append("token_id=%s")
        values.append(token_id)
    if amount:
        update_fields.append("amount=%s")
        values.append(amount)
    if asset_metadata:
        update_fields.append("asset_metadata=%s")
        values.append(asset_metadata)
    if is_display:
        update_fields.append("is_display=%s")
        values.append(is_display)
    if display_order:
        update_fields.append("display_order=%s")
        values.append(display_order)

    if not update_fields:
        return False  # 没有需要更新的字段
    try:
        sql = f"UPDATE digital_assets SET {', '.join(update_fields)} WHERE id=%s"
        values.append(asset_id)

        cur.execute(sql, tuple(values))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功更新
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)} 

def batch_insert_digital_assets(asset_list):
    """批量插入数字资产"""
    if not asset_list:
        return False

    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO digital_assets (user_id, asset_type, contract_address, name, token_id, amount, asset_metadata, is_display, display_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [(asset["user_id"], asset["asset_type"], asset["contract_address"], asset.get("name"), asset.get("token_id"), 
                asset.get("amount"), asset.get("asset_metadata"), asset.get("is_display"), asset.get("display_order"))for asset in asset_list]

        cur.executemany(sql, values)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)} 

def batch_update_digital_assets(asset_updates):
    """批量更新数字资产"""
    if not asset_updates:
        return False

    cur = mysql.connection.cursor()
    try:
        for asset in asset_updates:
            asset_id = asset.get("id")
            if not asset_id:
                continue

            update_fields = []
            values = []

            if "asset_type" in asset:
                update_fields.append("asset_type=%s")
                values.append(asset["asset_type"])
            if "contract_address" in asset:
                update_fields.append("contract_address=%s")
                values.append(asset["contract_address"])
            if "name" in asset:
                update_fields.append("name=%s")
                values.append(asset["name"])
            if "token_id" in asset:
                update_fields.append("token_id=%s")
                values.append(asset["token_id"])
            if "amount" in asset:
                update_fields.append("amount=%s")
                values.append(asset["amount"])
            if "asset_metadata" in asset:
                update_fields.append("asset_metadata=%s")
                values.append(asset["asset_metadata"])
            if "is_display" in asset:
                update_fields.append("is_display=%s")
                values.append(asset["is_display"])
            if "display_order" in asset:
                update_fields.append("display_order=%s")
                values.append(asset["display_order"])

            if update_fields:
                sql = f"UPDATE digital_assets SET {', '.join(update_fields)} WHERE id=%s"
                values.append(asset_id)
                cur.execute(sql, tuple(values))
    
            mysql.connection.commit()
            cur.close()
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}


def delete_digital_asset(asset_id):
    """删除数字资产"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE digital_assets SET data_status=1 WHERE id=%s", (asset_id,))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功删除
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}


def delete_digital_asset_by_user_id(user_id):
    """根据用户id删除其所有的数字资产"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE digital_assets SET data_status=1 WHERE user_id=%s", (user_id,))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功删除
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}
