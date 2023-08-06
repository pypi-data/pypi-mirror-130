# -*- coding: utf-8 -*-
# __author__ = "Casey"  395280963@qq.com
# Date: 2021-12-01  Python:3.6

import os
import json
import time
# import arrow
import random
import pymysql
import datetime
import traceback
from dbutils.pooled_db import PooledDB
import logging
import functools
from logging import handlers


def cprint(*args, c=31):  # 红色=31 绿色=32 黄色=33 蓝色=34 洋红=35 青色=36
    if len(args) == 0:
        print(f'\033[{c}m\033[0m', flush=True)
    if len(args) == 1:
        print(f'\033[{c}m{args[0]}\033[0m', flush=True)
    else:
        p_str = ""
        for arg in args:
            p_str = f"{p_str}{arg} "
        print(f'\033[{c}m{p_str}\033[0m', flush=True)


class Auto_insert():
    def __init__(self, host='127.0.0.1', username='root', password='', port=3306, db='test',
                 drop_column=None, pool_db=False, pool_num=10):
        if drop_column is None:
            drop_column = ["id"]
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.db = db
        self.pool_db = pool_db
        self.drop_column = drop_column  # 表删除字段
        self.pool_num = pool_num
        self.conn, self.cursor = self.sql_connect()
        self.table_name_list = self.get_db_name()
        self.column_list = self.get_columns()
        self.ping()

    def sql_connect(self):
        if self.pool_db:
            sql_pool = PooledDB(pymysql, self.pool_num, host=self.host, user=self.username, passwd=self.password,
                                db=self.db, port=3306, charset='utf8', use_unicode=True)
            conn = sql_pool.connection()
        else:
            conn = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.db,
                                   port=self.port, charset='utf8')
        cursor = conn.cursor()
        return conn, cursor

    def get_db_name(self):
        sql = f"select table_name from information_schema.tables where table_schema='{self.db}'"
        self.cursor.execute(sql)
        db_list = self.cursor.fetchall()
        db_list = [data[0] for data in db_list]
        return db_list

    def get_columns(self):
        item = {}
        for table_name in self.table_name_list:
            sql = f"select column_name from information_schema.columns where table_name='{table_name}' and table_schema='{self.db}'"
            self.cursor.execute(sql)
            column_list = self.cursor.fetchall()
            column_list = [data[0] for data in column_list]
            insert_columns = [data for data in column_list if data not in self.drop_column]
            item[table_name] = insert_columns
        return item

    def ping(self):
        error_count = 0
        while True:
            try:
                conn, cursor = self.sql_connect()
                return conn, cursor
            except Exception as e:
                fs = traceback.format_exc(chain=False)
                print(f"数据库连接失败,等待5s重试连接, error:{fs}")
                time.sleep(5)

                error_count += 1
                if error_count > 5:
                    print(f"数据库连接失败, 连接已断开! host:{self.host}, error:{fs}")
                    return None, None
                print(f"数据库连接失败, 正在尝试第 {error_count} 次重新连接... host:{self.host} ")

    def insert_data(self, item, table_name):
        """    插入 mysql 数据
        :param item为字典，数据库字段与内容对应
        :param table_name:
        :return:
        """
        sql_conn, cursor = self.ping()
        if item and sql_conn and cursor:
            item_key = self.column_list.get(table_name)
            if item_key:
                item_values = [
                    f"'{item.get(key)}'" if isinstance(item.get(key), str) else f"{item.get(key)}".replace("None",
                                                                                                           "NULL") for
                    key in item_key]
                insert = f"insert ignore into {table_name}({','.join(item_key)}) values({','.join(item_values)})"
                cursor.execute(insert)
                sql_conn.commit()
                print(f"****************   table_name:{table_name} insert data success   ****************")
            else:
                raise ValueError(f"不存在表:{table_name}")
        else:
            if not cursor or not sql_conn:
                with open('error_insert_data.txt', 'a', encoding='utf8')as f:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
                print("数据库连接异常，未插入数据字段保存在 error_insert_data.txt")
            else:
                print("item is None")
        cursor.close()
        sql_conn.close()

    def update_data(self, item, table_name):
        """   更新 mysql数据
        :param  item示例 {
        xxx:xxx,
        xxx:xxx,
        update_id:{
            'key':xxx,
            'value':xxx
        }
        }:
        :param table_name: 表名
        :return:
        """
        sql_conn, cursor = self.ping()
        if item and sql_conn and cursor:
            item_key = self.column_list.get(table_name)
            if item_key:
                if item.get('update_id'):
                    update_id_data = item.pop('update_id')
                    update_item_key = [key for key in item.keys()]
                    update_item_values = [
                        f"'{item.get(key)}'" if isinstance(item.get(key), str) else f"{item.get(key)}".replace("None",
                                                                                                               "NULL")
                        for key in update_item_key]
                    update_content = ''
                    for i in range(len(update_item_key)):
                        update_content += f'{update_item_key[i]}' + '=' + f'{update_item_values[i]}' + ','
                    update = f"UPDATE {table_name} SET {update_content.rstrip(',')} WHERE {update_id_data.get('key')}={update_id_data.get('value')}"
                    cursor.execute(update)
                    sql_conn.commit()
                    print(f"****************   table_name:{table_name} update data success   ****************")
                else:
                    raise ValueError('不存在更新的key: update_id')
            else:
                raise ValueError(f"不存在表:{table_name}")
        else:
            if not cursor or not sql_conn:
                with open('error_insert_data.txt', 'a', encoding='utf8')as f:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
                print("数据库连接异常，未插入数据字段保存在 error_insert_data.txt")
            else:
                print("item is None")
        cursor.close()
        sql_conn.close()


# 自定义日志文件写入
level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}
logger_initialized = {}


class Logger(object):
    def __init__(self, name="root", log_dir="./logs", print_out=True, file_out=True):
        os.makedirs(log_dir, exist_ok=True)
        self.name = name
        self.print_out = print_out
        self.file_out = file_out
        self.debug = self.get_logger(level="debug", log_dir=log_dir).debug
        self.info = self.get_logger(level="info", log_dir=log_dir).info
        self.warning = self.get_logger(level="warning", log_dir=log_dir).warning
        self.error = self.get_logger(level="error", log_dir=log_dir).error
        self.crit = self.get_logger(level="crit", log_dir=log_dir).critical

    @functools.lru_cache()
    def get_logger(self, level, log_dir):
        logger_name = f"{self.name}_{level}"
        logger = logging.getLogger(logger_name)
        if logger_name in logger_initialized:
            return logger
        for logger_name_ in logger_initialized:
            if logger_name.startswith(logger_name_):
                return logger

        filename = f"{log_dir}/{level}.log"
        formatter = logging.Formatter(
            '\033[36m[%(asctime)s] \033[32m[%(filename)s:%(lineno)4d] \033[35m%(levelname)s: %(message)s\033[0m',
            datefmt="%Y/%m/%d %H:%M:%S")  # 设置日志输出格式
        logger.setLevel(level_relations.get(level))  # 设置日志级别

        if self.print_out:
            print_handler = logging.StreamHandler()  # 往屏幕上输出
            print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
            logger.addHandler(print_handler)  # 把对象加到logger里
        if self.file_out:
            # file_handler = handlers.TimedRotatingFileHandler(filename=filename, when='D', backupCount=backCount,
            #                                                  encoding='utf-8')
            file_handler = handlers.RotatingFileHandler(filename=filename, mode='a', maxBytes=100 * 1024 * 1024,
                                                        backupCount=3, encoding='utf-8')
            file_handler.setFormatter(formatter)  # 设置文件里写入的格式
            logger.addHandler(file_handler)
        logger_initialized[logger_name] = True
        return logger


def yesterday_time():
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    return yesterday
