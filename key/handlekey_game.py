import time
class HandleKey(object):

    def __init__(self, tup_value, timefieldname):
        self.tup_value = tup_value
        self.timestamp_list = self.timestamp_list_solt(timefieldname)
        self.game_id = self.game_id_solt()
        self.channel = self.channel()

    def channel(self):
        if self.tup_value.has_key('ChannelID'):
            channel = self.tup_value["ChannelID"]
        else:
            channel = "all"
        return channel

    def timestamp_list_format(self, timestamp_format_list, timefieldname):
        timestamp_list = ['all']
        timestamp = timefieldname
        time_struct = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        for timestamp_format in timestamp_format_list:
            timestamp_list.append(time.strftime(timestamp_format, time_struct))
        return timestamp_list

    def timestamp_list_solt(self, timefieldname):
        timestamp_format_list = ["%Y", "%Y%m", "%Y%m%d", "%Y%m%d%H"]
        timestamp_list = self.timestamp_list_format(timestamp_format_list, timefieldname)
        return timestamp_list

    def timestamp_solt(self, timefieldname):
        timestamp = timefieldname
        time_struct = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        timestamp = time.strftime("%Y%m%d", time_struct)
        return timestamp

    def game_id_solt(self):
        if self.tup_value.has_key('GameID'):
            game_id = self.tup_value['GameID']
        else:
            game_id = "ENG-HJDWC-001"
        return game_id

    def base_key_list(self, datatype):
        redis_key_list = []
        for timestamp in self.timestamp_list:
            redis_key = 'ROYAL:%s:%s:%s' % (datatype, self.game_id, timestamp)
            redis_key_list.append(redis_key)
        return redis_key_list

    def base_key(self, datatype, timefieldname):
        timestamp = self.timestamp_solt(timefieldname)
        redis_key = 'ROYAL:%s:%s:%s' % (datatype, self.game_id, timestamp)
        return redis_key

    def channel_key_list(self, datatype):
        redis_channel_key_list = []
        channel = self.channel
        for timestamp in self.timestamp_list:
            redis_channel_key = 'ROYAL:%s:%s:%s:%s' % (datatype, self.game_id, timestamp, channel)
            redis_channel_key_list.append(redis_channel_key)
        return redis_channel_key_list

    def channel_key(self, datatype, timefieldname):
        timestamp = self.timestamp_solt(timefieldname)
        channel = self.channel
        redis_channel_key = 'ROYAL:%s:%s:%s:%s' % (datatype, self.game_id, timestamp, channel)
        return redis_channel_key

    def loginaccount_key(self):
        loginaccount_key = 'ROYAL:LOGINACCOUNT:%s:all' % (self.game_id)
        return loginaccount_key

    def firstlogin_key(self, date):
        game_id = self.game_id
        channel = self.channel
        firstlogin_key = 'ROYAL:FIRSTLOGIN:%s:%s:%s' % (game_id, date, channel)
        return firstlogin_key

    def payaccount_key_list(self):
        redis_key_list = []
        timestamp_format_list = ["%Y", "%Y%m", "%Y%m%d", "%Y%m%d%H", "%Y%m%d%H%M%S"]
        timestamp_list = self.timestamp_list_format(timestamp_format_list, 'TimeStamp')
        for timestamp in timestamp_list:
            redis_key = 'ROYAL:%s:%s:%s' % ("PAYACCOUNT", self.game_id, timestamp)
            redis_key_list.append(redis_key)
        return redis_key_list

    def payaccount_key(self):
        game_id = self.game_id
        payaccount_key = 'ROYAL:PAYACCOUNT:%s:all' % (game_id)
        return payaccount_key
