#-*-coding:utf8-*-
#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.payhandlelogic import PayHandleLogic
import logging




log = logging.getLogger('test_kafka')
class PayBolt(SimpleBolt):

    
    def process_tuple(self,tup):
         value = tup.values
         log.debug("kafka获取到的数据为:%s" % (value))
         pay_handle_logic_obj = PayHandleLogic(value)
         log.debug(u"开始付费账号处理!!!!")
         pay_handle_logic_obj.account()
         log.debug(u"开始付费次数处理!!!!")
         pay_handle_logic_obj.count('PAYCOUNT')
         log.debug(u"开始付费人数处理!!!!")
         pay_handle_logic_obj.num('PAYNUM','UUID')
         log.debug(u"开始付费金额处理!!!!")
         pay_handle_logic_obj.sum('PAYSUM', 'Amount')
         log.debug(u"开始付费行为处理!!!!")
         pay_handle_logic_obj.behavior()

    

if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/test_pay.log',
                format="%(asctime)s[%(levelname)s][%(lineno)d]%(message)s",
                filemode='a',
    )
    PayBolt().run()
