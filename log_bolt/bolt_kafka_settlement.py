#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.sethandlelogic import SetHandleLogic
import logging


log = logging.getLogger('test_kafka')
class SetBolt(SimpleBolt):
    
    
    def process_tuple(self,tup):
         value = tup.values
         #log.debug("kafka获取到的数据为:%s" % (value))
         #set_handle_logic_obj = SetHandleLogic(value)
         #log.debug(u"开启结算账号处理!!!!")
         #set_handle_logic_obj.account('SETTLEMENTACCOUNT','UUID')
         #log.debug(u"开启结算次数处理!!!!")
         #set_handle_logic_obj.count('SETTLEMENTCOUNT')
         #log.debug(u"开启结算人数处理!!!!")
         #set_handle_logic_obj.num('SETTLEMENTNUM','UUID')
         #log.debug(u"开启结算金额处理!!!!")
         #set_handle_logic_obj.sum('SETTLESUM', 'Amount')
         #log.debug(u"开启结算行为处理!!!!")
         #set_handle_logic_obj.behavior()



if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/test_settle.log',
                format="%(asctime)s[%(levelname)s][%(lineno)d]%(message)s",
                filemode='a',
    )
    SetBolt().run()
