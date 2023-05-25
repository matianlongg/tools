# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/5/25 16:35 
# @Author  : mtl
# @Desc    : ***
# @File    : operation.py
# @Software: PyCharm
import argparse
import sqlite3
from prompt_toolkit import PromptSession
def exec_sql(sql: str):
    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 执行查询语句
        cursor.execute(sql)

        # 获取查询结果
        results = cursor.fetchall()

        # 打印查询结果
        for row in results:
            print(row)

        # 提交更改
        conn.commit()

    except sqlite3.Error as e:
        print("Error executing SQL query:", e)


def show_all_tables():
    sql = "SELECT name FROM sqlite_master WHERE type='table';"
    exec_sql(sql)


# 创建命令行参数解析器
parser = argparse.ArgumentParser(description="SQLPython - A command-line tool for executing SQL queries.")
parser.add_argument("db_file", help="Path to the SQLite database file")
# 解析命令行参数
args = parser.parse_args()
# 连接到 SQLite 数据库
conn = sqlite3.connect(args.db_file)  # 根据实际路径替换
# 获取数据库名称
db_name = conn.execute("PRAGMA database_list;").fetchone()[2]
# 创建 PromptSession 对象
session = PromptSession()
print("Welcome to SQLPython!")
print(f"Connected to database: {db_name}")
print("Enter '1' to show all tables.")
while True:
    # 读取命令行输入
    sql_query: str = session.prompt("SQL> ")
    if sql_query.lower() == 'exit':
        # 如果输入 exit，则退出程序
        break
    if sql_query == '1':
        show_all_tables()
    else:
        # 判断最后一个字符是否为分号
        if sql_query.strip().endswith(';'):
            exec_sql(sql_query)
        else:
            # 换行输入下一行
            while True:
                sql_query += '\n' + session.prompt("... ")
                # 判断最后一个字符是否为分号
                if sql_query.strip().endswith(';'):
                    sql_query = sql_query.replace('\n', '')
                    exec_sql(sql_query)
                    break
# 关闭数据库连接
conn.close()
