import time

class HandleField(object):

    def __init__(self, tup_value):
        self.tup_value = tup_value

    def channel(self):
        if self.tup_value.has_key('ChannelID'):
            channel = self.tup_value["ChannelID"]
        else:
            channel = "ALL"
        return channel

    def channel_list(self):
        field_list = ['ALL']
        channel = self.channel()
        field_list.append(channel)
        return field_list

    def channel_uuid(self):
        uuid = self.tup_value["uuid"]
        channel = "ALL"
        field = '%s:%s' % (channel, uuid)
        return field

    def channel_uuid_list(self):
        field_list = []
        uuid = self.tup_value["UUID"]
        channel = self.channel()
        field_list.append('%s:%s' % (channel, uuid))
        field_list.append('ALL:%s' % (uuid,))
        return field_list

    def channel_day_list(self, day):
        field_list = []
        channel = self.channel()
        field_list.append('%s:%s' % (channel, day))
        field_list.append('ALL:%s' % (day,))
        return field_list

    def channel_kindld_list(self):
        field_list = ['ALL']
        kindle = self.tup_value["gameKindId"]
        channel = self.channel()
        field_list.append('%s:%s' % (channel, kindle))
        return field_list
   
    def type_serverid(self, type_value):
        field_list = []
        serverid = self.tup_value["serverID"]
        field_list.append('%s:%s' % (type_value, serverid))
        field_list.append('%s:ALL' % (type_value,))
        return field_list
