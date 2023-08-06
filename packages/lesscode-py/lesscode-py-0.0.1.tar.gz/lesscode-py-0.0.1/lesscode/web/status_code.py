# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2021/11/9 4:47 下午
# Copyright (C) 2021 The lesscode Team

from typing import Tuple


class StatusCode:
    """
    StatusCode 统一请求返回状态码
    # A表示错误来源于用户，比如参数错误，用户安装版本过低，用户支付超时等问题；
    # B表示错误来源于当前系统，往往是业务逻辑出错，或程序健壮性差等问题；
    # C表示错误来源于第三方服务
    """

    # *响应服务请求的状态码与说明
    SUCCESS = ("00000", "请求成功")
    FAIL = ("99999", "请求失败")
    USER_VALIDATE_FAIL = ("A0001", "用户端错误")
    USER_REGISTER_FAIL = ("A0100", "用户注册错误")
    USER_NAME_VALIDATE_FAIL = ("A0110", "用户名校验失败")
    USER_NAME_EXIST = ("A0111", "用户名已存在")
    USER_NAME_INVALID = ("A0112", "用户名包含特殊字符")
    PASSWORD_VALIDATE_FAIL = ("A0120", "密码校验失败")
    PASSWORD_LENGTH_VALID = ("A0121", "密码长度不够")
    SHORT_MESSAGE_VALID_FAIL = ("A0130", "短信验证码错误")
    VALIDATE_CODE_ERROR = ("A0131", "验证码错误！")
    USER_LOGIN_EXCEPTION = ("A0200", "用户登陆异常")
    USER_ACCOUNT_NOT_EXIST = ("A0201", "用户账户不存在")
    REQUEST_PARAM_ERROR = ("A0300", "用户请求参数错误")
    INVALID_USER_INPUT = ("A0301", "无效的用户输入")
    REQUIRED_PARAM_IS_EMPTY = ("A0310", "请求缺少必要参数:{}")
    INVALID_TIME_STAMP = ("A0311", "非法的时间戳参数")
    USER_INPUT_INVALID = ("A0312", "用户输入内容非法")
    VALIDATE_CODE_EXPIRE = ("A0400", "验证码过期")
    FORM_VALIDATE_FAIL = ("A0401", "表单校验失败")
    PARAM_VALIDATE_FAIL = ("A0402", "参数校验失败")
    PARAM_BIND_FAIL = ("A0403", "参数绑定失败")
    PHONE_NUM_NOT_FOUND = ("A0404", "找不到该用户，手机号码有误")
    PHONE_ALREADY_REGISTER = ("A0405", "手机号已经注册")
    BUSINESS_FAIL = ("B0000", "{}")
    ACCESS_DENIED = ("B0001", "访问权限不足")
    RESOURCE_DISABLED = ("B0002", "资源被禁用")
    RESOURCE_NO_AUTHORITY = ("B0003", "该资源未定义访问权限")
    RESOURCE_NOT_FOUND = ("B0404", "访问资源不存在")
    INTERNAL_SERVER_ERROR = ("B0500", "服务器内部错误:{}")
    RESOURCE_EXIST = ("B0501", "{}已存在,确保唯一性，不可重复")
    TIMEOUT = ("B0100", "系统执行超时")
    STRIKE_RECOVERY = ("B0200", "系统容灾系统被触发")
    RPC_INVOKE_ERROR = ("C0001", "调用第三方服务出错")
    SERVER_ERROR = ("C0002", "服务器内部错误")
    UNKNOWN_ERROR = ("C0003", "未知异常")

    @staticmethod
    def MESSAGE_FORMAT(status_code: Tuple[str, str], message):
        """
        用于自定义消息提示信息
        :param status_code: 状态码元祖
        :param message: 替换的消息内容
        :return:
        """
        return status_code[0], status_code[1].format(message)
