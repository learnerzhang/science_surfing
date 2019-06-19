#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-19 11:25
# @Author  : zhangzhen
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
import simplejson
from typing import Any, Text
import tempfile
import json
import os
import io


def json_to_string(obj: Any, **kwargs: Any) -> Text:
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


def write_json_to_file(filename: Text, obj: Any, **kwargs: Any) -> None:
    """Write an object as a json string to a file."""

    write_to_file(filename, json_to_string(obj, **kwargs))


def write_to_file(filename: Text, text: Text) -> None:
    """Write a text to a file."""

    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(str(text))


def read_file(filename: Text, encoding: Text = "utf-8-sig") -> Any:
    """Read text from a file."""
    with io.open(filename, encoding=encoding) as f:
        return f.read()


def read_json_file(filename: Text) -> Any:
    """Read json from a file."""
    content = read_file(filename)
    try:
        return simplejson.loads(content)
    except ValueError as e:
        raise ValueError("Failed to read json from '{}'. Error: "
                         "{}".format(os.path.abspath(filename), e))


def create_temporary_file(data: Any,
                          suffix: Text = "",
                          mode: Text = "w+") -> Text:
    """Creates a tempfile.NamedTemporaryFile object for data.

    mode defines NamedTemporaryFile's  mode parameter in py3."""

    encoding = None if 'b' in mode else 'utf-8'
    f = tempfile.NamedTemporaryFile(mode=mode, suffix=suffix,
                                    delete=False, encoding=encoding)
    f.write(data)

    f.close()
    return f.name