#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-18 17:50
# @Author  : zhangzhen
# @Site    : 
# @File    : ssr2json.py
# @Software: PyCharm
import argparse
import builtins
import collections
from typing import Text, Any, List
from pprint import pprint
import urllib.parse
import base64
import json
import os
import io

from logits.utils import read_file

ssr_template = {
    "index": 0,
    "random": False,
    "global": False,
    "enabled": True,
    "shareOverLan": False,
    "isDefault": False,
    "localPort": 1080,
    "pacUrl": None,
    "useOnlinePac": False,
    "reconnectTimes": 3,
    "randomAlgorithm": 0,
    "TTL": 0,
    "proxyEnable": False,
    "proxyType": 0,
    "proxyHost": None,
    "proxyPort": 0,
    "proxyAuthUser": None,
    "proxyAuthPass": None,
    "authUser": None,
    "authPass": None,
    "autoban": False,
    "configs": []
}


def read_ssr_file(filename: Text) -> Any:
    content = read_file(filename)

    lines = content.split('\n')
    return [line for line in lines if str(line).startswith('ssr:')]


def decode_base64(context):
    text = context.replace("-", "+").replace("_", "/")
    text = bytes(text, encoding="utf-8")
    missing_padding = 4 - len(text) % 4

    if missing_padding:
        text += b'=' * missing_padding
        try:
            return str(base64.decodebytes(text), encoding="utf-8")
        except:
            return ""


config_keys = {"remarks", "server", "server_port", "method", "obfs", "obfsparam", "remarks_base64", "password",
               "tcp_over_udp", "udp_over_tcp", "protocol", "obfs_udp", "enable", "group"}


def lines2cfgs(lines: List):
    configs = []
    for line in lines:
        cfg = collections.defaultdict(str)
        format_ssr_url = line[6:]
        # print(format_ssr_url)
        try:
            server, server_port, protocol, method, obfs, other = decode_base64(format_ssr_url).split(":")
            password_base64, param_base64 = other.split("/?")
            password = decode_base64(password_base64)
            params = param_base64.split("&")
            for param in params:
                k, v = param.split("=", 1)
                if v:
                    v = decode_base64(v)
                cfg[k] = v
            remarks_base64 = str(base64.b64encode(cfg['remarks'].encode('utf-8')), "utf-8")
            cfg.update({
                'server': server,
                'server_port': int(server_port),
                'protocol': protocol,
                'method': method,
                'obfs': obfs,
                'password': password,
                'remarks_base64': remarks_base64,
                'protocolparam': cfg.get('protoparam', ''),
                'enable': True,
            })
            configs.append(cfg)
        except builtins.ValueError:
            pass
        except ValueError:
            pass

    return configs


def text2cfg(text):
    if text:
        text = urllib.parse.unquote(text)
        lines = text.split('\n')
        cfgs = lines2cfgs(lines)
        ssr_template.update({'configs': cfgs})
    return ssr_template
