from handlelogic import HandleLogic
import time
from lib.mysql import mysql_operation

class PayHandleLogic(HandleLogic):

    def __init__(self, tup):
        self.tup_value = eval(tup[0][""])
        self.timefield = self.tup_value['TimeStamp']
        super(PayHandleLogic, self).__init__()

    def behavior(self):
        ret = super(PayHandleLogic, self).behavior()
        amount = self.tup_value['Amount']
        be_type = 'pay'
        strjson = str({'GameID': ret["game_id"], 'ChannelID': ret["channel"], 'Amount': amount})
        sql = """INSERT INTO behavior(uuid,type, strjson, date) VALUES ("%s", "%s", "%s", "%s")""" % (ret["uuid"], be_type, strjson, ret["timestamp"])
        mysql_operation_obj = mysql_operation('logserver')
        mysql_operation_obj.mysql_insert(sql)

    def account(self):
        account_key_list = self.handle_key_obj.payaccount_key_list(self.timefield)
        fields = self.handle_field_obj.channel_type_list("UUID")
        for account_key in account_key_list:
            for field in fields:
                self.redis_obj.hincrby(account_key, field)
