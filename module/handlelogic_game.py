import time

import redis

from field.handlefield_game import HandleField
from key.handlekey_game import HandleKey


class HandleLogic(object):
    redis_obj = redis.Redis(host='192.168.199.208', port=6379, db=0)

    def __init__(self):
        self.handle_key_obj = HandleKey(self.tup_value, self.timefield)
        self.handle_field_obj = HandleField(self.tup_value)

    def account(self, account):
        account_key_list = self.handle_key_obj.base_key_list(account)
        fields = self.handle_field_obj.channel_uuid_list()
        for account_key in account_key_list:
            for field in fields:
                self.redis_obj.hincrby(account_key, field)

    def count(self, count):
        count_key_list = self.handle_key_obj.base_key_list(count)
        fields = self.handle_field_obj.channel_list()
        for count_key in count_key_list:
            for field in fields:
                self.redis_obj.hincrby(count_key, field)

    def num(self, num):
        num_uuid_key_list = self.handle_key_obj.channel_key_list(num)
        fields = self.handle_field_obj.channel_list()
        uuid = self.tup_value['UUID']
        for num_uuid_key in num_uuid_key_list:
            num_uuid_key_split = num_uuid_key.split(':')
            num_uuid_key_del = num_uuid_key_split.pop()
            num_key = ':'.join(num_uuid_key_split)
            self.redis_obj.sadd(num_uuid_key, uuid)
            value = self.redis_obj.scard(num_uuid_key)
            for field in fields:
                self.redis_obj.hset(num_key, field, value)

    def sum(self, sum, sumfield):
        sum_key_list = self.handle_key_obj.base_key_list(sum)
        sumvaule = self.tup_value[sumfield]
        fields = self.handle_field_obj.channel_list()
        for sum_key in sum_key_list:
            for field in fields:
                self.redis_obj.hincrby(sum_key, field, sumvaule)

    def behavior(self):
        ret = {}
        if self.tup_value.has_key('ChannelID'):
            ret["channel"] = self.tup_value["ChannelID"]
        else:
            ret["channel"] = "ALL"
        if self.tup_value.has_key('GameID'):
            ret["game_id"] = self.tup_value['GameID']
        else:
            ret["game_id"] = "ENG-HJDWC-001"
        ret["uuid"] = self.tup_value['uuid']
        timestamp = self.timefield
        time_struct = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        ret["timestamp"] = time.strftime("%Y%m%d%H%M%S", time_struct)
        return ret
