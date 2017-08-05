import datetime


class DataNodeValue:
    def __init__(self, value=None, timestamp=None, data_node=None):
        self.id = None
        self.value = value
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now().isoformat()
        self.data_node = data_node

    def timestamp(self):
        return datetime.datetime.strptime(''.join(self.timestamp.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')

    def from_dict(_dict):
        d = DataNodeValue()
        d.value = _dict.get("value", None)
        d.timestamp = _dict.get("timestamp", None)
        d.id = _dict.get('id', None)
        return d

    def to_dict(self):
        _dict = self.__dict__.copy()
        _dict.pop('id', None)
        _dict.pop('data_node', None)
        return _dict

    def __str__(self):
        return self.to_dict().__str__()
