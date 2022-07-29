# -*- coding: utf-8 -*-
import code
import json


from exception.recommend_exception import RecommendException
from common.enums.error_code import ErrorCode as code


def assert_uid(uid):
    if uid is None or len(uid) == 0:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "参数uid:" + str(uid) + "不合法")


def assert_sessionid(session_id):
    if session_id is None or len(session_id) == 0:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "参数session_id:" + str(session_id) + "不合法")


def assert_in_range(param, range_list):
    if param is None or len(param) == 0:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "不合法")
    if not isinstance(range_list, list):
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "类型:" + str(range_list) + "不合法")
    if not param in range_list:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "不合法")


def assert_is_number(param):
    if param is None:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "不合法")
    if not param.isdigit():
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "类型不合法")


def assert_str_length(param, min_len, max_len):
    if param is None:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "不合法")
    if type(param) is not str:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "类型不合法")
    if len(param) < min_len or len(param) > max_len:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "param:" + str(param) + "长度不合法")


def get_param(request, param_name):
    if "GET" == request.method:
        param_data = request.args.get(param_name)
        if param_data is None:
            raise RecommendException(code.PARAM_ILLEGAL_ERROR, "参数" + param_name + "不存在")
    elif "POST" == request.method:
        body = json.loads(request.data, encoding="utf-8")
        param_data = body.get(param_name)
        if param_data is None:
            raise RecommendException(code.PARAM_ILLEGAL_ERROR, "参数" + param_name + "不存在")
    return param_data


def get_ip(request):
    ip = request.headers.get("x-forwarded-for")
    if ip is None or len(ip) == 0 or "unknown" in ip:
        ip = request.headers.get("WL-Proxy-Client-IP")
    if ip is None or len(ip) == 0 or "unknown" in ip:
        ip = request.remote_addr
    return ip


def get_params(request, param_name):
    if "GET" == request.method:
        return request.args.get(param_name)
    elif "POST" == request.method:
        return request.form.getlist(param_name)[0]


# 尝试获取参数，不强制参数必须存在，如果不存在返回空
def try_get_param(request, param_name):
    if "GET" == request.method:
        param_data = request.args.get(param_name)
        if param_data is None:
            param_data = ""
    elif "POST" == request.method:
        param_list = request.form.getlist(param_name)
        param_data = param_list[0]
        if param_data is None or len(param_data.strip()) == 0:
            raise RecommendException(code.PARAM_ILLEGAL_ERROR, "参数" + param_name + "不存在")
    return param_data.strip()


def get_req_body(request):
    if "GET" == request.method:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "不支持GET方法")
    elif "POST" == request.method:
        json_data = json.loads(request.get_data(as_text=True))
        return json_data


def get_header_param_no_check(request, param_name):
    param_data = request.headers.get(param_name)
    return param_data


def get_header_param_check(request, param_name):
    param_data = request.headers.get(param_name)
    if param_data is None or len(param_data.strip()) == 0:
        raise RecommendException(code.PARAM_ILLEGAL_ERROR, "请求头参数" + param_name + "不存在")
    return param_data


def get_param_not_check(request, param_name):
    """
    取值不校验
    """
    param_data = None
    if "GET" == request.method:
        param_data = request.args.get(param_name)
    elif "POST" == request.method:
        param_list = request.form.getlist(param_name)
        if len(param_list) > 0:
            param_data = param_list[0]
    if '' == param_data:
        param_data = None
    if ' ' == param_data:
        param_data = None
    return param_data