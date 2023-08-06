# -*- coding: utf-8 -*-
# @author: YuHuiMing
# @file: strings.py
# @time: 2021/7/19
# @desc:
from urllib.parse import urlparse


class Dict2Obj(object):
    """dict to obj"""

    def __init__(self, d):
        self.__dict__['d'] = d

    def __getattr__(self, key):
        value = self.__dict__['d'][key]
        if isinstance(value, dict):
            return Dict2Obj(value)
        return value


def parse_mysql_string(mysql_string):
    """
    parse mysql connect string
    : mysql_string mysql+pymysql://root:sr@12345@192.168.150.98:3306/yqn_da_platform?charset=utf8
    """
    parser = urlparse(mysql_string)
    # assert all([getattr(parser, "username"), getattr(parser, "password"), getattr(parser, "hostname"), getattr(parser, "path"),
    #             getattr(parser, "hostname"), getattr(parser, "port"), getattr(parser, "scheme")]), "mysql connect string format error"
    return Dict2Obj(dict(
        sql=parser.scheme.split("+")[0] if parser.scheme else "",
        package=parser.scheme.split("+")[1] if parser.scheme else "",
        mysql_username=parser.username if parser.username else "",
        mysql_password=parser.password if parser.password else "",
        mysql_host=parser.hostname if parser.hostname else "",
        mysql_port=parser.port if parser.port else "",
        mysql_database=parser.path.replace("/", "") if parser.path else "",
        mysql_charset=parser.query.split("=")[1] if parser.query else "utf8",
    ))


if __name__ == '__main__':
    # conn_str = "mysql+pymysql://root:sr@12345@192.168.150.98:3306/yqn_da_platform?charset=utf8"
    conn_str = "mysql+pymysql://root:sr@12345@192.168.150.98:3306/yqn_da_platform?charset=utf8"
    sql_conf = parse_mysql_string(conn_str)
    print(sql_conf.sql)
    print(sql_conf.package)
    print(sql_conf.mysql_username)
    print(sql_conf.mysql_password)
    print(sql_conf.mysql_host)
    print(sql_conf.mysql_port)
    print(sql_conf.mysql_database)
    print(sql_conf.mysql_charset)