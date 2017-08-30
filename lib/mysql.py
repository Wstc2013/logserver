import MySQLdb
import logging

log = logging.getLogger('test_kafka')

class mysql_operation(object):

    def __init__(self, db):
        self.db_obj = MySQLdb.connect(host='192.168.199.208', user='root', passwd='niku@2017', db=db, port=3306)
        self.cur = self.db_obj.cursor()

    def mysql_insert(self, sql):
        try:
            self.cur.execute(sql)
            self.db_obj.commit()
        except Exception as e:
            log.debug(str(e))
            self.db_obj.rollback()
        self.db_obj.close()

    def mysql_select_single(self, sql):
        try:
            self.cur.execute(sql)
            ret = self.cur.fetchone()
        except Exception as e:
            pass
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
