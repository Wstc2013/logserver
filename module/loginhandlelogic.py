#-*-coding:utf8-*-
from handlelogic import HandleLogic
import time,datetime
from lib.mysql import mysql_operation
import logging
log = logging.getLogger('test_kafka')


class LoginHandleLogic(HandleLogic):

    def __init__(self, tup):
        self.tup_value = eval(tup[0][""])
        self.timefield = self.tup_value['TimeStamp']
        super(LoginHandleLogic, self).__init__()


    def firstlogin(self, firstlogin, type_value):
            s_value = ''
            first_type_key = self.handle_key_obj.channel_key(firstlogin, self.timefield)
            log.debug("用于存放首登用户或首登设备的key为:%s" % (first_type_key))
            first_key_list = self.handle_key_obj.base_key_list(firstlogin)
            account_key = self.handle_key_obj.account_key(firstlogin)
            account_field = self.handle_field_obj.channel_type(type_value)
            log.debug("登陆的账号key:%s,field:%s" % (account_key,account_field))
            fields = self.handle_field_obj.channel_list()
            log.debug("首登key:%s,field:%s" % (first_key_list,fields))
            if type_value == 'UUID':
                s_value = self.tup_value['UUID']
            elif type_value == 'IMEI':
                s_value = self.tup_value['DeviceInfo']['IMEI']
            if not self.redis_obj.hexists(account_key, account_field):
                log.debug("该登陆账号不存在为首次登陆")
                self.redis_obj.sadd(first_type_key, s_value)
                log.debug("将%s放入当天首登集合中%s" % (s_value,first_type_key))
                for first_key in first_key_list:
                    for field in fields:
                        self.redis_obj.hincrby(first_key, field)

    def date_day_count(self, time_struct, offset_day):
        date_day = []
        for day in offset_day:
            delta = datetime.timedelta(days=day-1)
            n_date = time_struct - delta
            date = n_date.strftime('%Y%m%d')
            date_day.append({'date': date, 'day': day})
        return date_day

    def retained(self, retained, type_value):
            s_value = ''
            datatype = ''
            retained_key = self.handle_key_obj.base_key(retained, self.timefield)
            log.debug("留存key为:%s" % (retained_key))
            timestamp = self.timefield
            timestamp = timestamp.split(' ')[0]
            log.debug("当前时间为:%s" % (timestamp))
            if type_value == 'UUID':
                s_value = self.tup_value['UUID']
                datatype = 'FIRSTLOGIN'
            elif type_value == 'IMEI':
                s_value = self.tup_value['DeviceInfo']['IMEI']
                datatype = 'FIRSTLOGINDEVICE'
            time_struct = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
            offset_day = [2, 3, 7, 15, 30]
            log.debug("记录2,3,7,15,30留数据")
            date_days = self.date_day_count(time_struct, offset_day)
            log.debug("2,3,7,15留对应的时间为:%s" % (date_days))
            for date_day in date_days:
                firstlogin_key = self.handle_key_obj.firstlogin_key(datatype, date_day['date'])
                log.debug("某留对应的首登集合key为:%s" % (firstlogin_key))
                fields = self.handle_field_obj.channel_day_list(date_day['day'])
                log.debug("某留对应的fields为:%s" % (fields))
                log.debug("判断用户或设备在某留的首登集合里")
                if self.redis_obj.sismember(firstlogin_key, s_value):
                    for field in fields:
                        log.debug(retained_key)
                        self.redis_obj.hincrby(retained_key, field)

    def behavior(self):
        ret = super(LoginHandleLogic, self).behavior()
        account_key = self.handle_key_obj.account_key("LOGINACCOUNT")
        field = self.handle_field_obj.channel_type("UUID")
        be_type = 'login'
        if not self.redis_obj.hexists(account_key, field):
            be_type = 'register'
        strjson = str({'GameID': ret["game_id"], 'ChannelID': ret["channel"]})
        sql = """INSERT INTO behavior(uuid,type, strjson, date) VALUES ("%s", "%s", "%s", "%s")""" % (ret["uuid"], be_type, strjson, ret["timestamp"])
        log.debug("用户行为执行的sql语句为:%s" % (sql))
        #print sql
        mysql_operation_obj = mysql_operation('logserver')
        mysql_operation_obj.mysql_insert(sql)
