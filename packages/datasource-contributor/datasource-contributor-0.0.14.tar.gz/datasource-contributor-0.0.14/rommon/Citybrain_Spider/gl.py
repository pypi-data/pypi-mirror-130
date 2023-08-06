# -*- coding: utf-8 -*-

global_dict = {}


def init():  # 初始化
    global global_dict
    global_dict['TEST_SSO_DOMAIN'] = "http://192.168.12.156:32003"
    global_dict['TEST_DOMAIN'] = "http://192.168.12.156:32002"
    global_dict['PRODUCTION_SSO_DOMAIN'] = "http://sso.citybrain.org"
    global_dict['PRODUCTION_DOMAIN'] = "http://www.citybrain.org"
    global_dict['CURRENT_SSO_DOMAIN'] = global_dict['TEST_SSO_DOMAIN']
    global_dict['CURRENT_DOMAIN'] = global_dict['TEST_DOMAIN']


def set_value(key, value):
    """
    定义一个全局变量
    :param key:
    :param value:
    :return:
    """
    global_dict[key] = value


def get_value(key, def_value=None):
    """
    获取一个全局变量，不存在则返回默认值
    :param key:
    :param def_value:
    :return:
    """
    try:
        return global_dict[key]
    except KeyError:
        return def_value


# 全局变量
# TEST_SSO_DOMAIN = "http://192.168.12.156:32003"
# TEST_DOMAIN = "http://192.168.12.156:32002"
# PRODUCTION_SSO_DOMAIN = "http://sso.citybrain.org"
# PRODUCTION_DOMAIN = "http://www.citybrain.org"
# CURRENT_SSO_DOMAIN = ""
# CURRENT_DOMAIN = ""
