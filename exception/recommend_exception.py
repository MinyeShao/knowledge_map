# -*- coding:utf-8 -*-


class RecommendException(Exception):
    def __init__(self, error_code, error_desc):
        self.error_code = error_code
        self.error_desc = error_desc

    def __str__(self):
        return "error code:" + str(self.error_code) + ", error_desc:" + str(self.error_desc)

    def get_errorcode(self):
        return self.error_code

    def get_errordesc(self):
        return self.error_desc
