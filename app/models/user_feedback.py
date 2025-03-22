from app import mysql
from app.common.tools import datetime_serializer

def get_feedback_by_user_id(user_id):
    """根据用户 ID 获取所有反馈"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_user_feedback WHERE rel_user_id = %s AND data_status=0 order by create_time desc", (user_id,))
    feedbacks = cur.fetchall()
    cur.close()
    temp = {}
    result = []
    if(feedbacks is not None):
        for item in feedbacks:
            temp = {
                "id": item[0],
                "rel_user_id": item[1],
                "feedback_content": item[2],
                "rel_record_id": item[3],
                "satisfaction": item[4],
                "handle_status": item[5],
                "data_status": item[6],
                "job_number": item[7],
                "remark": item[8],
                "create_time": datetime_serializer(item[9]),
                "update_time": datetime_serializer(item[10])
            }
            result.append(temp.copy())
    return result

def get_feedback_by_id(feedback_id):
    """通过 ID 获取单个用户反馈"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_user_feedback WHERE id = %s AND data_status=0", (feedback_id,))
    item = cur.fetchone()
    cur.close()
    if item is None:
        return None
    result = {
        "id": item[0],
        "rel_user_id": item[1],
        "feedback_content": item[2],
        "rel_record_id": item[3],
        "satisfaction": item[4],
        "handle_status": item[5],
        "data_status": item[6],
        "job_number": item[7],
        "remark": item[8],
        "create_time": datetime_serializer(item[9]),
        "update_time": datetime_serializer(item[10])
    }
    return result

def add_user_feedback(rel_user_id, feedback_content, rel_record_id=None, satisfaction=None):
    """添加新的用户反馈"""
    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO t_user_feedback (rel_user_id, feedback_content, rel_record_id, satisfaction)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (rel_user_id, feedback_content, rel_record_id, satisfaction))
        mysql.connection.commit()
        cur.close()
        return cur.lastrowid  
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}


def update_user_feedback(feedback_id, handle_status=None, job_number=None, remark=None):
    """更新用户反馈处理状态"""
    cur = mysql.connection.cursor()
    update_fields = []
    values = []

    if handle_status is not None:
        update_fields.append("handle_status=%s")
        values.append(handle_status)
    if job_number is not None:
        update_fields.append("job_number=%s")
        values.append(job_number)
    if remark is not None:
        update_fields.append("remark=%s")
        values.append(remark)

    if not update_fields:
        return False  # 没有需要更新的字段
    try:
        sql = f"UPDATE t_user_feedback SET {', '.join(update_fields)}, update_time=CURRENT_TIMESTAMP WHERE id=%s"
        values.append(feedback_id)

        cur.execute(sql, tuple(values))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功更新
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}

def batch_insert_user_feedback(feedback_list):
    """批量插入用户反馈"""
    if not feedback_list:
        return False

    cur = mysql.connection.cursor()
    try:
        sql = """
            INSERT INTO t_user_feedback (rel_user_id, feedback_content, rel_record_id, satisfaction)
            VALUES (%s, %s, %s, %s)
        """
        values = [(feedback["rel_user_id"], feedback["feedback_content"], feedback.get("rel_record_id"), feedback.get("satisfaction"))
                for feedback in feedback_list]

        cur.executemany(sql, values)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}

def batch_update_user_feedback(feedback_updates):
    """批量更新用户反馈处理状态"""
    if not feedback_updates:
        return False

    cur = mysql.connection.cursor()
    try:
        for feedback in feedback_updates:
            feedback_id = feedback.get("id")
            if not feedback_id:
                continue

            update_fields = []
            values = []

            if "handle_status" in feedback:
                update_fields.append("handle_status=%s")
                values.append(feedback["handle_status"])
            if "job_number" in feedback:
                update_fields.append("job_number=%s")
                values.append(feedback["job_number"])
            if "remark" in feedback:
                update_fields.append("remark=%s")
                values.append(feedback["remark"])

            if update_fields:
                sql = f"UPDATE t_user_feedback SET {', '.join(update_fields)}, update_time=CURRENT_TIMESTAMP WHERE id=%s"
                values.append(feedback_id)
                cur.execute(sql, tuple(values))

        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}

def delete_user_feedback(feedback_id):
    """删除用户反馈"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE t_user_feedback SET data_status=1 WHERE id=%s", (feedback_id,))
        mysql.connection.commit()
        cur.close()
        return cur.rowcount > 0  # 返回是否成功删除
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return {"error": str(e)}
