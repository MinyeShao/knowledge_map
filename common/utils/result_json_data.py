# -*- coding:utf-8 -*-
import json
from collections import OrderedDict


class ResultJsonData:

    def __init__(self):
        self.json_data = OrderedDict()

    def put(self, key, value):
        self.json_data[key] = value

    def to_json(self):
        return self.json_data

    def to_string(self):
        return json.dumps(self.json_data)


if __name__ == "__main__":
    resultJsonData: ResultJsonData = ResultJsonData()
    list_1 = []
    for i in range(10):
        dict_1 = {}
        dict_1["1"] = 2
        list_1.append(dict_1)
    resultJsonData.put("a", "1")
    resultJsonData.put("a1", list_1)
    print(resultJsonData.to_string())
