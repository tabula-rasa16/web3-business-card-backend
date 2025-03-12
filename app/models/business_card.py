from app import mysql
from app.common.tools import datetime_serializer

def get_business_cards_by_user_id(user_id):
    """根据用户id获取其名片"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM business_cards WHERE user_id = %s and data_status=0", (user_id,))
    cards = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(cards is not None):
        for item in cards:
            temp = {
                "id": item[0],
                "user_id": item[1],
                "display_name": item[2],
                "company": item[3],
                "job_title": item[4],
                "website_url": item[5],
                "portfolio_url": item[6],
                "debox_account": item[7],
                "email": item[8],
                "phone": item[9],
                "data_status": item[10],
                "created_at": datetime_serializer(item[11]),
                "updated_at": datetime_serializer(item[12])
            }
            result.append(temp.copy())
    return result

def get_business_card_by_id(card_id):
    """通过 ID 获取单个名片"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM business_cards WHERE id = %s and data_status=0", (card_id,))
    card = cur.fetchone()
    cur.close()
    return card

def add_business_card(user_id, display_name, company, job_title, website_url, portfolio_url, debox_account, email, phone):
    """添加新的名片"""
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO business_cards 
        (user_id, display_name, company, job_title, website_url, portfolio_url, debox_account, email, phone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, display_name, company, job_title, website_url, portfolio_url, debox_account, email, phone))
    mysql.connection.commit()
    cur.close()

def update_business_card(card_id, display_name, company, job_title, website_url, portfolio_url, debox_account, email, phone):
    """更新名片信息"""
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE business_cards 
        SET display_name=%s, company=%s, job_title=%s, website_url=%s, portfolio_url=%s, debox_account=%s, email=%s, phone=%s
        WHERE id=%s
    """, (display_name, company, job_title, website_url, portfolio_url, debox_account, email, phone, card_id))
    mysql.connection.commit()
    cur.close()

def delete_business_card(card_id):
    """删除名片"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE business_cards SET data_status=1 WHERE id=%s", (card_id,))
    mysql.connection.commit()
    cur.close()


# 社交帐号相关
def get_social_accounts_by_user_id(user_id):
    """根据用户 ID 获取其关联的社交账号"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, platform,account_handle ,profile_url ,created_at FROM social_accounts WHERE user_id = %s AND data_status = 0 order by platform asc", (user_id,))
    accounts = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(accounts is not None):
        for item in accounts:
            temp = {
                "id": item[0],
                "platform": item[1],
                "account_handle": item[2],
                "profile_url": item[3],
                "created_at": datetime_serializer(item[4])
            }
            result.append(temp.copy())
    return result


def get_social_account_by_id(account_id):
    """通过 ID 获取单个社交账号"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM social_accounts WHERE id = %s AND data_status = 0", (account_id,))
    account = cur.fetchone()
    cur.close()
    return account


def add_social_account(user_id, platform, account_handle, profile_url=None):
    """添加社交账号"""
    cur = mysql.connection.cursor()
    sql = """
        INSERT INTO social_accounts (user_id, platform, account_handle, profile_url)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (user_id, platform, account_handle, profile_url))
    mysql.connection.commit()
    cur.close()
    return {"message": "Social account added successfully"}



def batch_add_social_accounts(accounts):
    """
    批量插入社交账号信息
    :param accounts: List[Tuple(user_id, platform, account_handle, profile_url)]
    :return: dict
    """
    # 参数格式
    '''
    [
        (1, 'twitter', '@user1', 'https://twitter.com/user1'),
        (2, 'github', 'user2', 'https://github.com/user2'),
        (3, 'linkedin', 'user3', 'https://linkedin.com/in/user3')
    ]
    '''

    if not accounts:
        return {"message": "No accounts to insert"}

    cur = mysql.connection.cursor()
    sql = """
        INSERT INTO social_accounts (user_id, platform, account_handle, profile_url)
        VALUES (%s, %s, %s, %s)
    """
    
    try:
        cur.executemany(sql, accounts)
        mysql.connection.commit()
        return {"message": f"{len(accounts)} social accounts added successfully"}
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cur.close()



def update_social_account(account_id, platform=None, account_handle=None, profile_url=None):
    """更新社交账号信息"""
    cur = mysql.connection.cursor()
    sql = "UPDATE social_accounts SET "
    updates = []
    params = []

    if platform:
        updates.append("platform = %s")
        params.append(platform)
    if account_handle:
        updates.append("account_handle = %s")
        params.append(account_handle)
    if profile_url:
        updates.append("profile_url = %s")
        params.append(profile_url)

    if not updates:
        return {"message": "No fields to update"}

    sql += ", ".join(updates) + " WHERE id = %s"
    params.append(account_id)

    cur.execute(sql, params)
    mysql.connection.commit()
    cur.close()
    return {"message": "Social account updated successfully"}


def batch_update_social_accounts(updates):
    """
    批量更新社交账号信息
    :param updates: List[Dict]，每个字典包含 id 及需更新的字段
    :return: dict
    """
    # 参数格式
    '''
    [
        {"id": 1, "platform": "twitter", "account_handle": "@new_user1"},
        {"id": 2, "profile_url": "https://github.com/new_user2"},
        {"id": 3, "platform": "linkedin", "account_handle": "new_user3", "profile_url": "https://linkedin.com/in/new_user3"}
    ]
    '''
    
    if not updates:
        return {"message": "No accounts to update"}

    cur = mysql.connection.cursor()
    try:
        for account in updates:
            account_id = account.get("id")
            if not account_id:
                continue  # 跳过无 ID 的数据

            fields = []
            values = []

            if "platform" in account:
                fields.append("platform = %s")
                values.append(account["platform"])
            if "account_handle" in account:
                fields.append("account_handle = %s")
                values.append(account["account_handle"])
            if "profile_url" in account:
                fields.append("profile_url = %s")
                values.append(account["profile_url"])

            if not fields:
                continue  # 如果没有字段需要更新，则跳过

            values.append(account_id)  # 添加 ID 作为 WHERE 条件
            sql = f"UPDATE social_accounts SET {', '.join(fields)}, updated_at = NOW() WHERE id = %s"
            cur.execute(sql, values)

        mysql.connection.commit()
        return {"message": f"{len(updates)} social accounts updated successfully"}
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cur.close()



def delete_social_account(account_id):
    """删除社交账号"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE social_accounts SET data_status=1 WHERE id = %s", (account_id,))
    mysql.connection.commit()
    cur.close()
    return {"message": "Social account deleted successfully"}


def batch_delete_social_accounts(user_id):
    """根据用户id批量删除社交账号"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE social_accounts SET data_status=1 WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return {"message": "Social accounts deleted successfully"}





