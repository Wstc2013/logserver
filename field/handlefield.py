import time

class HandleField(object):

    def __init__(self, tup_value):
        self.tup_value = tup_value

    def channel(self):
        if self.tup_value.has_key('ChannelID'):
            channel = self.tup_value["ChannelID"]
        else:
            channel = self.tup_value['DeviceInfo']['Channel']
        return channel

    def channel_list(self):
        field_list = ['ALL']
        channel = self.channel()
        field_list.append(channel)
        return field_list

    def channel_type(self, type_value):
        if type_value == 'UUID':
            s_value = self.tup_value["UUID"]
        elif type_value == 'IMEI':
            s_value = self.tup_value['DeviceInfo']['IMEI']
        channel = self.channel()
        field = '%s:%s' % (channel, s_value)
        return field

    def channel_type_list(self, type_value):
        field_list = []
        if type_value == 'UUID':
            s_value = self.tup_value["UUID"]
        elif type_value == 'IMEI':
            s_value = self.tup_value['DeviceInfo']['IMEI']
        channel = self.channel()
        field_list.append('%s:%s' % (channel, s_value))
        field_list.append('ALL:%s' % (s_value,))
        return field_list

    def channel_day_list(self, day):
        field_list = []
        channel = self.channel()
        field_list.append('%s:%s' % (channel, day))
        field_list.append('ALL:%s' % (day,))
        return field_list

    def channel_kindld_list(self):
        field_list = ['ALL']
        kindle = self.tup_value["gameroundID"]
        channel = self.channel()
        field_list.append('%s:%s' % (channel, kindle))
        field_list.append('ALL:%s' % (kindle,))
        return field_list
