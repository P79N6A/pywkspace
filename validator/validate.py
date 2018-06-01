#!/usr/bin/env python
# coding: utf-8
# Copyright © 2017 头条网 All Rights Reserved.
# duanlingling (duanlingling@bytedance.com)

from jsonschema import validate
import compiler
import logging
import sys
from util.schemaHandler import SchemaHandler
logger = logging.getLogger('validate')
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("out.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Validator():

    case_change = None

    def __init__(self, case_info):

        self.name = case_info.get('name')
        self.url = case_info.get('url')
        self.headers = case_info.get('headers')
        self.post_data = case_info.get('post_data')
        self.method = case_info.get('method')
        self.schema = case_info.get('schema')
        self.case_script = case_info.get('case_script')
        if not self.case_change:
            self.case_change = False


    def schema_validate(self, data):
        try:
            if isinstance(self.schema, dict):
                if len(self.schema) == 0:
                    sc = SchemaHandler()
                    self.schema = sc.json_to_schema(data)
                    self.case_change = True
            validate(data, self.schema)
        except Exception as ex:
            pattern = '.*\n\nFailed validating .* in schema.*:'
            import re
            if re.match(pattern, str(ex)):
                exceptinfo = re.match(pattern, str(ex)).group()
                exceptinfo = exceptinfo.replace('\n',' ')
            else:
                exceptinfo = str(ex)
            except_info = '[{0}] {1}'.format('JSON SCHEMA 校验失败 ', exceptinfo)
            logger.error('json schema validator failed: \n'.format(exceptinfo))
            raise Exception(except_info)

    def check_script(self, data):
        if not self.case_script:
            return
        try:
            value = self.case_script
            code = '#coding: utf8\n'
            code += 'def handle():\n'
            for line in value.split('\n'):
                code += '    ' + line + '\n'
            code += 'result = handle()'
            logger.info('code_validator:\n'.format(code))
            code = compiler.compile(self.case_script, '<string>', 'exec')
            exec(code, data)
        except:
            error = sys.exc_info()[0]
            info = '[代码校验失败] %s \n' % error
            logging.error('code validator: ', info)
            raise Exception(info)

        if 'result' in data:
            return data['result']
        return None