# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2021/11/10 7:52 下午
# Copyright (C) 2021 The lesscode Team
from lesscode.web.status_code import StatusCode


class BusinessException(RuntimeError):
    """
    BusinessException 统一异常类型，增加状态码信息
    """

    def __init__(self, status_code:StatusCode):
        super(BusinessException, self).__init__(status_code[1])
        self.status_code = status_code
