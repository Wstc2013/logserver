#-*-coding:utf8-*-
from handlelogic_game import HandleLogic
from lib import mysql
import configparser
import time
from lib.mysql import mysql_operation
import requests
import json
import logging
log = logging.getLogger('test_kafka')


class GameHandleLogic(HandleLogic):
    config = configparser.ConfigParser()
    config.read("config/commission.ini",encoding='utf-8')

    def __init__(self, tup):
        self.tup_value = self.tup_value_solt(tup)
        self.timefield = self.tiemfield_solt(self.tup_value['curTime'])
        super(GameHandleLogic, self).__init__()

    def tiemfield_solt(self, tiemfield):
        time_local = time.localtime(tiemfield)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def tup_value_solt(self, tup):
        new_value = tup[0]
        if '\xef\xbb\xbf' in new_value:
            value = eval(new_value)
        else:
            value = json.loads(new_value)
        return value

    def sum(self, sum, sumfield):
        sum_key_list = self.handle_key_obj.base_key_list(sum)
        log.debug("获取对应的key:%s" % (sum_key_list))
        sumvaule = self.tup_value[sumfield]
        log.debug("获取税收值为:%s" % (sumvaule))
        fields = self.handle_field_obj.channel_kindld_list()
        log.debug("获取每个key对应的field为:%s" %(fields))
        log.debug("开始税收处理")
        for sum_key in sum_key_list:
            for field in fields:
                self.redis_obj.hincrbyfloat(sum_key, field, sumvaule)

    def behavior(self):
        ret = super(GameHandleLogic, self).behavior()
        be_type = 'game'
        log.debug("行为类型为:%s" % (be_type))
        strjson = str({'GameID': ret["game_id"], 'ChannelID': ret["channel"]})
        log.debug("行为strjson为:%s" % (strjson))
        sql = """INSERT INTO behavior(uuid,type, strjson, date) VALUES ("%s", "%s", "%s", "%s")""" % (ret["uuid"], be_type, strjson, ret["timestamp"])
        mysql_operation_obj = mysql_operation('logserver')
        mysql_operation_obj.mysql_insert(sql)

    def commission(self):
        uuid = self.tup_value['uuid']
        game_id = "ENG-HJDWC-001"
        account_field = self.handle_field_obj.channel_uuid()
        timestamp = self.timefield
        time_struct = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        #timestamp = time.strftime("%Y%m%d%H%M%S", time_struct)
        timestamp_rbd = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        account_key = self.handle_key_obj.payaccount_key()
        kindld = str(self.tup_value['gameKindId'])
        if not self.redis_obj.hexists(account_key, account_field):
            return
        type_name = self.config.get(kindld, "Type")
        rate_id = 0
        while True:
            rate_list = self.config.get(kindld, 'Rates').split(';')
            log.debug(type_name)
            log.debug(rate_list)
            log.debug(self.tup_value['totalbet'])
            if  "BET" in type_name :
                log.debug("is bet")
                commission = self.tup_value['totalbet']*float(rate_list[rate_id])
            else:
                log.debug("is commission")
                commission = self.tup_value['servicerevenue']*float(rate_list[rate_id])
            log.debug(commission)
            select_ta = """SELECT iu from ta where ud='%s'""" % (uuid)
            mysql_operation_obj = mysql_operation('lpsystem')
            i_uuid = mysql_operation_obj.mysql_select_single(select_ta)
            if not i_uuid:
                return
            log.debug("###########################")
            select_rb = """SELECT * from rb where ud='%s'""" % (i_uuid)
            updata_rb = """UPDATE rb set am='%s' where ud='%s'""" % (commission, i_uuid)
            insert_rb = """INSERT INTO rb(ud,gi,am) VALUES ("%s", "%s", "%s")""" % (i_uuid, game_id, commission)
            mysql_operation_rb_obj = mysql_operation('lpsystem')
            mysql_operation_rb_obj.mysql_insert_updata(select_rb,insert_rb, updata_rb)
            insert_rbd = """INSERT INTO rbd(ud,gi,de,am) VALUES ("%s", "%s", "%s","%s")""" % (i_uuid, game_id, timestamp_rbd, commission)
            mysql_operation_rdb_obj = mysql_operation('lpsystem')
            mysql_operation_rdb_obj.mysql_insert(insert_rbd)
            if commission > 1000:
                msgcontent = "你推荐的玩家给您带来了佣金%s元，请您在佣金界面查收。加油多多推广，躺着也收钱。" % (commission)
                data = {'msgtitle': "佣金到账提醒", 'msgcontent': msgcontent,'uuid': uuid}
                url = self.config.get("main", 'MailUrl')
                try:
                    r = requests.post(url, data=json.dumps(data))
                except Exception as e:
                    pass #"r.json'
            uuid = i_uuid
            rate_id += rate_id

