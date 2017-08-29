from remoteclick.datanode_value import DataNodeValue
from remoteclick.value_type import ValueType


class DataNode:
    def __init__(self, name="", value_type=ValueType.NUMBER, unit="", keep_history=True, path="", read_only=True):
        self.name = name
        self.value_type = value_type
        self.unit = unit
        self.keep_history = keep_history
        self.path = path
        self.href = path
        self.read_only = read_only
        self.id = None
        self.values = {}

    def from_dict(_dict):
        d = DataNode()
        d.name = _dict.get("name", "")
        d.value_type = _dict.get("valueType", None)
        d.unit = _dict.get("unit", "")
        d.keep_history = _dict.get("keepHistory", False)
        d.path = _dict.get("path", "")
        d.href = _dict.get("href", "")
        d.read_only = _dict.get("readOnly", "")
        d.id = _dict.get("id", None)
        return d

    def to_dict(self):
        _dict = self.__dict__.copy()
        _dict.pop('id', None)
        _dict.pop('values', None)
        _dict.pop('href', None)
        return _dict

    def full_name(self):
        return self.path.strip("/") + "/" + self.name

    def new_value(self, value=None, timestamp=None):
        return DataNodeValue(value=value, timestamp=timestamp, data_node=self)

    def __str__(self):
        return self.to_dict().__str__()
