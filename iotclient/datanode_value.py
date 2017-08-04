import datetime


class DataNodeValue:
    def __init__(self, value=None, timestamp=None):
        self.id = None
        self.value = value
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now().isoformat()

    def from_dict(_dict):
        d = DataNodeValue()
        d.value = _dict.get("value", None)
        d.timestamp = _dict.get("timestamp", None)
        d.id = _dict.get('id', None)
        return d

    def to_dict(self):
        _dict = self.__dict__
        _dict.pop('id', None)
        return _dict

    def __str__(self):
        return self.__dict__.__str__()
