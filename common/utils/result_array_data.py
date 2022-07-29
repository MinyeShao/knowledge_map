# -*- coding:utf-8 -*-
import json


class ResultArrayData:

    def __init__(self):
        self.array_data = []

    def put(self, json_data):
        self.array_data.append(json_data)

    def to_json(self):
        return self.array_data

    def to_string(self):
        json_array = [json_data for json_data in self.array_data]
        return json.dumps(json_array)


if __name__ == "__main__":
    resultArrayData: ResultArrayData = ResultArrayData()
    resultArrayData.put({"a": 1})
    resultArrayData.put({"a": 2})
    print(resultArrayData.to_string())


