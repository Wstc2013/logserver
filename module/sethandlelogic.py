from handlelogic import HandleLogic
import time
from lib.mysql import mysql_operation

class SetHandleLogic(HandleLogic):

    def __init__(self, tup):
        self.tup_value = eval(tup[0][""])
        self.timefield = self.tup_value['SettlementTime']
        super(SetHandleLogic, self).__init__()


    def behavior(self):
        ret = super(SetHandleLogic, self).behavior()
        amount = self.tup_value['Amount']
        be_type = 'settlement'
        strjson = str({'GameID': ret["game_id"], 'ChannelID': ret["channel"], 'Amount': amount})
        sql = """INSERT INTO behavior(uuid,type, strjson, date) VALUES ("%s", "%s", "%s", "%s")""" % (ret["uuid"], be_type, strjson, ret["timestamp"])
        mysql_operation_obj = mysql_operation('logserver')
        mysql_operation_obj.mysql_insert(sql)
