import json
from hardware_interfaces.channels import ChannelInterface


class ChannelEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ChannelInterface):
            dict = o.__dict__
            dict['type'] = o.__name__

        return json.JSONEncoder.default(self, o)
