#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.sethandlelogic import SetHandleLogic
import logging


log = logging.getLogger('test_kafka')
class SetBolt(SimpleBolt):
    
    
    def process_tuple(self,tup):
         value = tup.values
         #log.debug(value)
         #set_handle_logic_obj = SetHandleLogic(value)
         #set_handle_logic_obj.account('SETTLEMENTACCOUNT','UUID')
         #set_handle_logic_obj.count('SETTLEMENTCOUNT')
         #set_handle_logic_obj.num('SETTLEMENTNUM','UUID')
         #set_handle_logic_obj.sum('SETTLESUM', 'Amount')
         #set_handle_logic_obj.behavior()



if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/test_settle.log',
                format="%(asctime)s[%(levelname)s][%(lineno)d]%(message)s",
                filemode='a',
    )
    SetBolt().run()
