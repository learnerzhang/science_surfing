#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-19 12:13
# @Author  : zhangzhen
# @Site    : 
# @File    : ssr2json_test.py
# @Software: PyCharm
import argparse

from logits.ssr2json import read_ssr_file, lines2cfgs, ssr_template
from logits.utils import write_json_to_file


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="ssr file path")
    parser.add_argument("--output", type=str, default="shadowsocksR.json", help="output config file path")

    return parser.parse_known_args()


FLAGS, unparsed = args()

def main():
    lines = read_ssr_file(FLAGS.path)
    cfgs = lines2cfgs(lines)
    ssr_template.update({'configs': cfgs})
    write_json_to_file(FLAGS.output, ssr_template)


if __name__ == '__main__':
    main()
