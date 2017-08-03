class ValueType:
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"


class DataNode:
    def __init__(self, name="", value_type=ValueType.NUMBER, unit="", keep_history=True, path=""):
        self.name = name
        self.value_type = value_type
        self.unit = unit
        self.keep_history = keep_history
        self.path = path
        self.href = path
        self.id = None

    def from_dict(_dict):
        d = DataNode()
        d.name = _dict["name"]
        d.value_type = _dict["valueType"]
        d.unit = _dict["unit"]
        d.keep_history = _dict["keepHistory"]
        d.path = _dict["path"]
        d.href = _dict["href"]
        d.id = _dict["id"]
        return d

    def to_dict(self):
        _dict = self.__dict__
        _dict.pop('id', None)
        return _dict

    def __str__(self):
        return self.__dict__.__str__()
