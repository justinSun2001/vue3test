import sqlite3
import csv
from pyecharts.charts import Bar, Line, Scatter, Pie
from pyecharts import options as opts
import pandas as pd
import base64

def get_conn():
    # 建立SQLite连接
    conn = sqlite3.connect("test.db")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def table_exists(table_name):
    conn, cursor = get_conn()
    cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    res = cursor.fetchone()[0]
    close_conn(conn, cursor)
    return res > 0

# def create_music_table(csv_file):
#     conn, cursor = get_conn()
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#         headers = next(csv_reader)  # 获取CSV文件的第一行作为表格的字段名
#         # 创建表格
#         cursor.execute(f"CREATE TABLE IF NOT EXISTS music (music_id INTEGER PRIMARY KEY AUTOINCREMENT,{', '.join(headers)});")
#     conn.commit()
#     close_conn(conn, cursor)
# def insert_data_from_csv(csv_file):
#     conn, cursor = get_conn()
#     # 检查表格是否已存在
#     if not table_exists("music"):
#         create_music_table(csv_file)
#         with open(csv_file, 'r', encoding='utf-8') as file:
#             csv_reader = csv.reader(file)
#             headers = next(csv_reader)  # 跳过标题行
#             for row in csv_reader:
#                 # 构造INSERT语句
#                 placeholders = ', '.join(['?'] * len(row))
#                 insert_sql = f"INSERT INTO music ({', '.join(headers)}) VALUES ({placeholders})"
#                 cursor.execute(insert_sql, row)
#         conn.commit()
#     else:
#         print("Table 'music' already exists. Skipping data insertion.")
#     close_conn(conn, cursor)
# insert_data_from_csv('creditcard.csv')

def create_user_table():
    conn, cursor = get_conn()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, school TEXT DEFAULT '',college TEXT DEFAULT '',major TEXT DEFAULT '',class TEXT DEFAULT '',name TEXT DEFAULT '',registration_time TEXT DEFAULT CURRENT_TIMESTAMP);")
    close_conn(conn, cursor)
def add_admin():
    conn, cursor = get_conn()
    if not table_exists("user"):
        create_user_table()
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("admin", "admin"))
        conn.commit()
    else:
        print("Table 'user' already exists. Skipping data insertion.")
    close_conn(conn, cursor)
add_admin()



def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，[{},{}]的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    conn.commit()
    close_conn(conn, cursor)
    return res

def get_user(username):
    # 防止SQL注入
    sql = "select user_id, username, password from user where username=?"
    res = query(sql, username)
    return res

def add_user(username, password):
    # 判断账号是否存在
    exit_sql = "select COUNT(user_id) from user where username=?"
    exit_res = query(exit_sql, username)

    if exit_res[0][0] > 0:
        return "300"
    else:
        # 防止SQL注入
        sql = "insert into user (username, password) VALUES (?, ?)"
        res = query(sql, username, password)
        return "200"

def get_user_id_by_username(username):
    conn, cursor = get_conn()
    cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
    result = cursor.fetchone()
    user_id = result[0] if result else None
    close_conn(conn, cursor)
    return user_id

# 用户个人信息
def get_user_info(user_id):
    # 执行 SQL 查询
    conn, cursor = get_conn()  # 假设这是你的数据库连接和游标获取函数
    # 执行嵌套查询
    cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()  # 获取所有行
    # 准备存储数据的列表
    data = []
    # 获取列名（字段名）
    column_names = [desc[0] for desc in cursor.description]
    # 遍历每一行数据
    for row in rows:
        # 使用列名作为键，对应的数据值作为值，创建一个字典
        row_dict = dict(zip(column_names, row))
        data.append(row_dict)  # 将字典添加到数据列表中
    # 关闭连接
    close_conn(conn, cursor)

    return data
def update_user_info(user_id, key, value):
    # 执行 SQL 查询
    conn, cursor = get_conn()  # 假设这是你的数据库连接和游标获取函数
    # 根据 key 动态构建列名
    column_name = f'`{key}`'  # 使用 f-string 来构建列名，注意列名使用了反引号（`），这在某些数据库中是必需的
    # 构建 SQL 更新语句，使用 ? 作为 SQLite 的占位符
    sql = f"UPDATE user SET {column_name}=? WHERE user_id=?"
    # 执行 SQL 更新语句
    cursor.execute(sql, (value, user_id))
    conn.commit()
    # 执行嵌套查询
    cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()  # 获取所有行
    # 准备存储数据的列表
    data = []
    # 获取列名（字段名）
    column_names = [desc[0] for desc in cursor.description]
    # 遍历每一行数据
    for row in rows:
        # 使用列名作为键，对应的数据值作为值，创建一个字典
        row_dict = dict(zip(column_names, row))
        data.append(row_dict)  # 将字典添加到数据列表中
    # 关闭连接
    close_conn(conn, cursor)

    return data

# 后台数据
def get_user_num():
    conn, cursor = get_conn()  # 假设这是你的数据库连接和游标获取函数
    cursor.execute('SELECT COUNT(*) FROM user')
    # 获取查询结果
    count_result = cursor.fetchone()
    # 由于查询返回的是单行单列的结果，我们可以从元组中取出这个值
    user_count = count_result[0]
    print(f"The number of entries in the 'user' table is: {user_count}")
    # 关闭连接
    close_conn(conn, cursor)
    return user_count
# 用户账户名密码
def get_user_data(page_size,current_page):
    # 计算偏移量
    offset = (current_page - 1) * page_size
    # 执行 SQL 查询
    conn, cursor = get_conn()  # 假设这是你的数据库连接和游标获取函数
    # 执行分页查询
    cursor.execute(f"SELECT * FROM user LIMIT ? OFFSET ?", (page_size, offset))
    rows = cursor.fetchall()  # 获取所有行
    # 准备存储数据的列表
    data = []
    # 获取列名（字段名）
    column_names = [desc[0] for desc in cursor.description]
    # 遍历每一行数据
    for row in rows:
        # 使用列名作为键，对应的数据值作为值，创建一个字典
        row_dict = dict(zip(column_names, row))
        data.append(row_dict)  # 将字典添加到数据列表中
    # 关闭连接
    close_conn(conn, cursor)

    return data

def delete_user_data(ids):
    print(ids)
    # 连接到数据库
    conn, cursor = get_conn() 
    # 构建 WHERE 子句
    where_clause = ' OR '.join([f"user_id = ?" for _ in ids])
    # 构建删除 SQL 语句
    delete_sql = f"DELETE FROM user WHERE {where_clause};"
    print(delete_sql)
    # 执行删除操作
    try:
        cursor.execute(delete_sql, ids)  # 直接传递 ids 列表作为参数
        conn.commit()  # 提交事务
        conn.close()  # 关闭连接
        return "user deleted successfully"
    except sqlite3.Error as e:
        conn.rollback()  # 回滚事务
        conn.close()  # 关闭连接
        return f"Failed to delete user: {e}"
    
def upload_user_data(data):
    # 连接到数据库
    conn, cursor = get_conn() 
    password = data.get('password')
    username = data.get('username')
    # 执行插入操作
    try:
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()  # 关闭连接
        return "user uploaded successfully"
    except sqlite3.Error as e:
        conn.close()  # 关闭连接
        return f"Failed to upload user: {e}"
    
def update_user_data(data):
    # 连接到数据库
    conn, cursor = get_conn() 
    user_id = data.get('user_id')
    password = data.get('password')
    username = data.get('username')
    # 执行更新操作
    try:
        cursor.execute("UPDATE user SET username=?, password=? WHERE user_id=?", (username, password, user_id))
        conn.commit()
        conn.close()  # 关闭连接
        return "user updated successfully"
    except sqlite3.Error as e:
        conn.close()  # 关闭连接
        return f"Failed to update user: {e}"