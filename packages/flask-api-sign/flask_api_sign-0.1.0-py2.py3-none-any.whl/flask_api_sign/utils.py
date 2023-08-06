# -*- coding: utf-8 -*-
# @author: juforg
# @email: juforg@sina.com
# @date: 2020/04/06
#      SJ编程规范
# 命名：
#    1. 见名思意，变量的名字必须准确反映它的含义和内容
#    2. 遵循当前语言的变量命名规则
#    3. 不要对不同使用目的的变量使用同一个变量名
#    4. 同个项目不要使用不同名称表述同个东西
#    5. 函数/方法 使用动词+名词组合，其它使用名词组合
# 设计原则：
#    1. KISS原则： Keep it simple and stupid !
#    2. SOLID原则： S: 单一职责 O: 开闭原则 L: 迪米特法则 I: 接口隔离原则 D: 依赖倒置原则
#

from flask import current_app
import hashlib

from flask_api_sign.api_sign_manager import ApiSign
import base64


def _md5(pwd):
    return hashlib.md5(pwd).hexdigest()


def _get_apisign_manager():
    try:
        return current_app.extensions['flask-api-sign']
    except KeyError:  # pragma: no cover
        raise RuntimeError("You must initialize a ApiSignManager with this flask "
                           "application before using this method")


def signature(api_sign: ApiSign):
    apisign_manager = _get_apisign_manager()
    sorted_params = sorted(api_sign.dict().items(), key=lambda param_list: param_list[0])
    query_str = ''
    for (k, v) in sorted_params:
        query_str += f"{k}={v}&"
    query_str += apisign_manager.get_and_check_app_secret(api_sign.app_id)
    sign = _md5(query_str.encode('utf-8')).upper()
    return sign


def base64url_decode(input_str):
    return base64.urlsafe_b64decode(input_str)


def base64url_encode(input_str):
    return base64.urlsafe_b64encode(input_str).replace(b'=', b'')
