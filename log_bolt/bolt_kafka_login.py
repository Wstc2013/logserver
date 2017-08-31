#-*-coding:utf8-*-
#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.loginhandlelogic import LoginHandleLogic
import logging

log = logging.getLogger('test_kafka')
class LoginBolt(SimpleBolt):
    
    
    def process_tuple(self,tup):
         value = tup.values
         log.debug("kafka获取到的数据为:%s" % (value))
         login_handle_logic_obj = LoginHandleLogic(value)
         log.debug("开始用户首登处理!!!!")
         login_handle_logic_obj.firstlogin('FIRSTLOGIN', 'UUID')
         log.debug("开始用户行为处理!!!!")
         login_handle_logic_obj.behavior()
         log.debug("开始用户登陆账号处理!!!!")
         login_handle_logic_obj.account('LOGINACCOUNT', 'UUID')
         log.debug("开始用户登陆次数处理!!!!")
         login_handle_logic_obj.count('LOGINCOUNT')
         log.debug("开始用户登陆人数处理!!!!")
         login_handle_logic_obj.num('LOGINNUM', 'UUID')
         log.debug("开始用户登陆留存处理!!!!")
         login_handle_logic_obj.retained('RETAINED', 'UUID')
         log.debug("开始设备首登处理!!!!")
         login_handle_logic_obj.firstlogin('FIRSTLOGINDEVICE', 'IMEI')
         log.debug("开始设备登陆账号处理!!!!")
         login_handle_logic_obj.account('ACCOUNTDEVICE', 'IMEI')
         log.debug("开始设备登陆次数处理!!!!")
         login_handle_logic_obj.count('COUNTDEVICE')
         log.debug("开始设备登陆个数处理!!!!")
         login_handle_logic_obj.num('NUMDEVICE', 'IMEI')
         log.debug("开始设备留存处理!!!!")
         login_handle_logic_obj.retained('RETAINEDDEVICE', 'IMEI')




if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/test_login.log',
                format="%(asctime)s[%(levelname)s][%(process)d][%(thread)d][%(lineno)d]%(message)s",
                filemode='a',
    )
    LoginBolt().run()
