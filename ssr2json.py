#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-18 17:50
# @Author  : zhangzhen
# @Site    : 
# @File    : ssr2json.py
# @Software: PyCharm
import argparse
import builtins
import json
from typing import Text, Any, List
from pprint import pprint
import base64
import codecs

config_template = {
    "remarks": "",
    "server": "0.0.0.0",
    "server_ipv6": "::",
    "server_port": 8388,
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "password": "m",
    "method": "aes-128-ctr",
    "protocol": "auth_aes128_md5",
    "protocol_param": "",
    "obfs": "tls1.2_ticket_auth_compatible",
    "obfs_param": "",
    "speed_limit_per_con": 0,
    "speed_limit_per_user": 0,
    "additional_ports": {},
    "additional_ports_only": False,
    "timeout": 120,
    "udp_timeout": 60,
    "dns_ipv6": False,
    "connect_verbose_info": 0,
    "redirect": "",
    "fast_open": False,
}

alias = {
    'obfsparam': 'obfs_param',
    'protoparam': 'protocol_param',
}


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


def ssr2json(text: Text, out: Text):
    format_ssr_url = text[6:]
    try:
        server, server_port, protocol, method, obfs, other = decode_base64(format_ssr_url).split(":")
        password_base64, param_base64 = other.split("/?")
        password = decode_base64(password_base64)
        params = param_base64.split("&")
        for param in params:
            k, v = param.split("=", 1)
            if v:
                v = decode_base64(v)
                if k in alias and alias[k] in config_template:
                    config_template[alias[k]] = v
                else:
                    config_template[k] = v

        remarks_base64 = str(base64.b64encode(config_template['remarks'].encode('utf-8')), "utf-8")
        config_template.update({
            'server': server,
            'server_port': int(server_port),
            'protocol': protocol,
            'method': method,
            'obfs': obfs,
            'password': password,
            'remarks_base64': remarks_base64,
            'enable': True,
        })
        json.dump(config_template, codecs.open(out, 'w+'))
        pprint(config_template)
        print("保存配置文件{}".format(out))
    except builtins.ValueError:
        pass
    except ValueError:
        pass


def create_argument_parser():
    parser = argparse.ArgumentParser(description='parse incoming text')
    parser.add_argument('-s', "--ssr", type=str, required=True, help='ssr text')
    parser.add_argument('-o', "--out", type=str, default='ssr.json', help='ssr config')
    return parser


if __name__ == '__main__':
    cmdline_args = create_argument_parser().parse_args()
    ssr2json(text=cmdline_args.ssr, out=cmdline_args.out)
