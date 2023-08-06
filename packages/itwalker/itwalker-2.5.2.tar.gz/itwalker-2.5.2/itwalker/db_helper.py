import pymysql, psycopg2
from dbutils.pooled_db import PooledDB
import psycopg2.extras
import logging
from enum import Enum

pool = {}


class DBFormat(Enum):
    TP = "tuple"
    DT = "dict"


class SafeConnect:
    def __init__(self, tp, format):
        db_cls, db_conf, log_cls = tp
        self.db_cls = db_cls
        self.db_conf = db_conf
        self.log_cls = log_cls
        self.format = format

    def __enter__(self):
        global pool
        try:
            dbname = self.db_cls.__name__
            if dbname not in pool:
                self.log_cls.debug(f"初始化{dbname}数据池")
                pool[dbname] = PooledDB(creator=self.db_cls, maxconnections=4, **self.db_conf)
            self.conn = pool[dbname].connection()
            self.log_cls.debug("数据库链接打开")
            if self.format == DBFormat.TP:
                cursor = self.conn.cursor()
            else:
                if dbname == pymysql.__name__:
                    cursor = self.conn.cursor(pymysql.cursors.DictCursor)
                else:
                    cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return self.conn, cursor
        except Exception as e:
            self.log_cls.error(e)
            self.log_cls.error("数据库连接失败")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        self.log_cls.debug("数据库链接关闭")


class DBBase:
    __db_cls, __db_conf, __log_cls = None, None, None

    def __init__(self, db_cls, db_conf, log_cls):
        self.__db_cls = db_cls
        self.__db_conf = db_conf
        self.__log_cls = log_cls
        self.__tp = (db_cls, db_conf, log_cls)

    def __executeParam(self, cursor, sql, Param):
        if not Param:
            self.__log_cls.info(sql)
            return cursor.execute(sql)
        else:
            if isinstance(Param, dict):
                self.__log_cls.info(sql % Param)
                return cursor.execute(sql, Param)
            else:
                self.__log_cls.info(sql % Param)
                return cursor.execute(sql % Param)

    def handleMany(self, result):
        if not result:
            return []
        else:
            check_item = result[0]
            if isinstance(check_item, dict):
                check_value = False
                for v in check_item.values():
                    if v or isinstance(v, int):
                        check_value = True
                        break
                return [dict(v) for v in result] if check_value else []
            else:
                check_value = False
                for v in check_item.values():
                    if v or isinstance(v, int):
                        check_value = True
                        break
                return result if check_value else []

    def handleSingle(self, result):
        if not result:
            return None
        else:
            return result

    def Query(self, sql, Param=None, format=DBFormat.DT):
        with SafeConnect(self.__tp, format) as (conn, cursor):
            try:
                self.__executeParam(cursor, sql, Param)
                result = cursor.fetchall()
                return self.handleMany(result)
            except Exception as e:
                self.__log_cls.error(e)
                raise e
            finally:
                self.__log_cls.debug("query over")

    def QuerySingle(self, sql, Param=None, format=DBFormat.DT):
        with SafeConnect(self.__tp, format) as (conn, cursor):
            try:
                self.__executeParam(cursor, sql, Param)
                result = cursor.fetchone()
                return self.handleSingle(result)
            except Exception as e:
                self.__log_cls.error(e)
                raise e
            finally:
                self.__log_cls.debug("querysingle over")

    def ExcuteSql(self, sql, Param=None):
        global db_cls, db_conf, log_cls
        with SafeConnect(self.__tp, DBFormat.TP) as (conn, cursor):
            try:
                self.__executeParam(cursor, sql, Param)
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                self.__log_cls.error(e)
                raise e
            finally:
                self.__log_cls.info("excutesql over")

    def ExecuteMany(self, sql, Param=None):
        global db_cls, db_conf, log_cls
        if not isinstance(Param, list):
            raise Exception("Param must is list")
        with SafeConnect(self.__tp, DBFormat.TP) as (conn, cursor):
            try:
                cursor.executemany(sql, Param)
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                self.__log_cls.error(e)
                raise e
            finally:
                self.__log_cls.info("executemany over")


class PgHelper(DBBase):
    def __init__(self, pgsql_conf, new_log=logging):
        if new_log is logging:
            logging.basicConfig(level=logging.NOTSET)
        super(PgHelper, self).__init__(psycopg2, pgsql_conf, new_log)

    def handleMany(self, result):
        if not result:
            return []
        else:
            check_item = result[0]
            if isinstance(check_item, psycopg2.extras.DictRow):
                check_value = False
                for v in check_item.values():
                    if v or isinstance(v, int):
                        check_value = True
                        break
                return [dict(v) for v in result] if check_value else []
            else:
                check_value = False
                for v in check_item.values():
                    if v or isinstance(v, int):
                        check_value = True
                        break
                return result if check_value else []

    def handleSingle(self, result):
        if not result:
            return None
        else:
            return dict(result)


class MysqlHelper(DBBase):

    def __init__(self, mysql_conf, new_log=logging):
        if new_log is logging:
            logging.basicConfig(level=logging.NOTSET)
        super(MysqlHelper, self).__init__(pymysql, mysql_conf, new_log)
