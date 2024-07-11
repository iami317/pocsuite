#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@Author  :  hao
@File    :  loader.py
@Time    :  2020/7/16 下午3:43
'''

import importlib.machinery
import importlib.util
from importlib.abc import Loader

from lib.util import get_md5


def load_string_to_module(code_string, fullname=None, log=None):
    '''name
    加载字符串到模块中
    :param code_string:
    :param fullname:
    :return:
    '''
    try:
        module_name = 'poc_{0}'.format(get_md5(code_string)) if fullname is None else fullname
        file_path = 'Poc://{0}'.format(module_name)
        poc_loader = PocLoader(module_name, file_path)
        poc_loader.set_data(code_string)
        spec = importlib.util.spec_from_file_location(module_name, file_path, loader=poc_loader)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except ImportError:
        error_msg = 'load module "{}" failed!'.format(fullname)
        log.error(error_msg)
        raise


class PocLoader(Loader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self, filename):
        if self.data:
            data = self.data
        else:
            with open(filename, encoding='utf-8') as f:
                data = f.read()
        return data

    def exec_module(self, module):
        filename = self.path
        poc_code = self.get_data(filename)
        obj = compile(poc_code, filename, 'exec', dont_inherit=True)
        exec(obj, module.__dict__)
