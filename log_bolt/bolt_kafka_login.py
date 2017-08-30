#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.loginhandlelogic import LoginHandleLogic
import logging

log = logging.getLogger('test_kafka')
class LoginBolt(SimpleBolt):
    
    
    def process_tuple(self,tup):
         value = tup.values
         log.debug(value)
         login_handle_logic_obj = LoginHandleLogic(value)
         login_handle_logic_obj.firstlogin('FIRSTLOGIN', 'UUID')
         login_handle_logic_obj.behavior()
         login_handle_logic_obj.account('LOGINACCOUNT', 'UUID')
         login_handle_logic_obj.count('LOGINCOUNT')
         login_handle_logic_obj.num('LOGINNUM', 'UUID')
         login_handle_logic_obj.retained('RETAINED', 'UUID')
         login_handle_logic_obj.firstlogin('FIRSTLOGINDEVICE', 'IMEI')
         login_handle_logic_obj.account('ACCOUNTDEVICE', 'IMEI')
         login_handle_logic_obj.count('COUNTDEVICE')
         login_handle_logic_obj.num('NUMDEVICE', 'IMEI')
         login_handle_logic_obj.retained('RETAINEDDEVICE', 'IMEI')




if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/test_login.log',
                format="%(asctime)s[%(levelname)s][%(lineno)d]%(message)s",
                filemode='a',
    )
    LoginBolt().run()
