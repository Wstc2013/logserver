#-*-coding:utf8-*-
#!/usr/bin/env python
from __future__ import absolute_import
from pyleus.storm import SimpleBolt
from module.gamehandlelogic import GameHandleLogic
import logging


log = logging.getLogger('test_kafka')
class GameBolt(SimpleBolt):
    
    
    def process_tuple(self,tup):
         value = tup.values
         log.debug("kafka获取到的数据为:%s" % (value))
         game_handle_logic_obj = GameHandleLogic(value)
         log.debug("开始税收处理!!!!")
         game_handle_logic_obj.sum('REVENUESUM', 'servicerevenue')
         log.debug("开始系统输赢处理!!!!")
         game_handle_logic_obj.sum('SYSSCORE', 'totalbet')
         log.debug("开始佣金行为处理!!!!")
         game_handle_logic_obj.behavior()
         log.debug("开始佣金处理!!!!")
         game_handle_logic_obj.commission()



if __name__ == '__main__':
    logging.basicConfig(
                level=logging.DEBUG,
                filename='/tmp/gameresult.log',
                format="%(asctime)s[%(levelname)s][%(process)d][%(thread)d][%(lineno)d]%(message)s",
                filemode='a',
    )
    GameBolt().run()
