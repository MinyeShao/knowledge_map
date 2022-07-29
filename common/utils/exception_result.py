# -*- coding: utf-8 -*-
import json
import random
import traceback
from collections import OrderedDict
from exception.recommend_exception import RecommendException
from common.enums.error_code import ErrorCode as code


class ExceptionResult(object):

    def __init__(self, exception):
        self.json_error = OrderedDict()
        self.log_id = random.randint(100000000, 999999999)
        self.exception = exception

    def get_json(self):
        print(self.exception.args)
        print(traceback.format_exc())
        json_result = OrderedDict()
        if isinstance(self.exception, RecommendException):
            if isinstance(self.exception.get_errorcode(), str):
                json_result['code'] = self.exception.get_errorcode()
            else:
                json_result['code'] = self.exception.get_errorcode().value
            json_result['desc'] = self.exception.get_errordesc()
        else:
            json_result['code'] = code.PARAM_INTERNEL_ERROR.value
            json_result['desc'] = "internel error"
        json_result['log_id'] = self.log_id
        return json.dumps(json_result, ensure_ascii=False)
