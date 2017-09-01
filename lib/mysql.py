#-*-coding:utf8-*-
import MySQLdb
import logging
import configparser

log = logging.getLogger('test_kafka')

class mysql_operation(object):
    config = configparser.ConfigParser()
    config.read("config/config.ini",encoding='utf-8')
    hostname = config.get("mysql", "hostname")
    user = config.get("mysql", "username")
    password = config.get("mysql", "password")
    port = int(config.get("mysql", "port"))

    def __init__(self, db):
        self.db_obj = MySQLdb.connect(host=self.hostname, user=self.user, passwd=self.password, db=db, port=self.port)
        self.cur = self.db_obj.cursor()

    def mysql_insert(self, sql):
        try:
            self.cur.execute(sql)
            self.db_obj.commit()
        except Exception as e:
            log.debug("数据库插入报错:str(e)")
            self.db_obj.rollback()
        self.db_obj.close()

    def mysql_select_single(self, sql):
        try:
            self.cur.execute(sql)
            ret = self.cur.fetchone()
        except Exception as e:
            log.debug("数据库查询报错:str(e)")
        self.db_obj.close()
        ret = ret[0]
        return ret

    def mysql_insert_updata(self, select_sql,insert_sql, updata_sql):
        select_ret = self.cur.execute(select_sql)
        log.debug(select_ret)
        if select_ret:
        	self.cur.execute(updata_sql)
        else: 
            self.cur.execute(insert_sql)
            self.db_obj.commit()
        self.db_obj.close()
