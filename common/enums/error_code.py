# -*- coding:utf-8 -*-
from enum import Enum


class ErrorCode(Enum):
    SUCCESS = "0"
    SESSION_TIMEOUT_ERROR = "1"
    PARAM_ILLEGAL_ERROR = "2"
    DATA_NOT_EXIST = "3"
    DATA_CANOT_MODIFY = "4"

    # 内部数据错误
    INTERNEL_ERROR = "400"
    PARAM_INTERNEL_ERROR = "500"
