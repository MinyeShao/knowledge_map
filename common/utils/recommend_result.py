import random
from collections import OrderedDict

from common.utils.result_array_data import ResultArrayData
from common.utils.result_json_data import ResultJsonData
from exception.recommend_exception import RecommendException
from common.enums.error_code import ErrorCode as code
import json


class RecommendResult:

    def __init__(self, code, result_data, page_id=None, page_size=None, page_total=None, total_size=None):
        self.error_code = code
        self.log_id = str(random.randint(100000000, 999999999))
        self.result_data = result_data
        self.page_id = page_id
        self.page_size = page_size
        self.page_total = page_total
        self.total_size = total_size

    def get_json(self):
        """
            page_ 放在result外面
        """
        json_result = OrderedDict()
        json_result['code'] = self.error_code
        json_result['log_id'] = self.log_id

        result_dict = {}
        if self.page_id is not None:
            result_dict['page_id'] = self.page_id

        if self.page_size is not None:
            result_dict['page_size'] = self.page_size

        if self.page_total is not None:
            result_dict['page_total'] = self.page_total

        if self.total_size is not None:
            result_dict['total_size'] = self.total_size
        if isinstance(self.result_data, ResultJsonData):
            result_dict["data"] = self.result_data.to_json()
            json_result['desc'] = "success"
        elif isinstance(self.result_data, ResultArrayData):
            result_dict["data"] = self.result_data.to_json()
            json_result['desc'] = "success"
        elif isinstance(self.result_data, OrderedDict):
            result_dict["data"] = self.result_data
            json_result['desc'] = "success"
        elif isinstance(self.result_data, dict):
            result_dict["data"] = self.result_data
            json_result['desc'] = "success"
        elif isinstance(self.result_data, list):
            result_dict["data"] = self.result_data
            json_result['desc'] = "success"
        elif isinstance(self.result_data, str):
            result_dict["data"] = self.result_data
            json_result['desc'] = "success"
        else:
            raise RecommendException(code.PARAM_INTERNEL_ERROR, "内部参数错误")
        json_result["result"] = result_dict
        return json.dumps(json_result, ensure_ascii=False)
