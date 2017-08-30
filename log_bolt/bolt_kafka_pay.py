#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.payhandlelogic import PayHandleLogic
import logging




log = logging.getLogger('test_kafka')
class PayBolt(SimpleBolt):

    
    def process_tuple(self,tup):
         value = tup.values
         log.debug(value)
         pay_handle_logic_obj = PayHandleLogic(value)
         pay_handle_logic_obj.account()
         pay_handle_logic_obj.count('PAYCOUNT')
         pay_handle_logic_obj.num('PAYNUM','UUID')
         pay_handle_logic_obj.sum('PAYSUM', 'Amount')
         pay_handle_logic_obj.behavior()

    

if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/test_pay.log',
                format="%(asctime)s[%(levelname)s][%(lineno)d]%(message)s",
                filemode='a',
    )
    PayBolt().run()
