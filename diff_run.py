#!/usr/bin/env python
# coding: utf-8
# Copyright © 2017 头条网 All Rights Reserved.
# duanlingling (duanlingling@bytedance.com)

from validator.validate import Validator
from util.dataHandler import DataHandler
from util.requestHandler import *
import logging

logger = logging.getLogger('diff_run')
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("out.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DiffRun():

    def run(self):
        file_root = 'cases'
        d_data = DataHandler()
        filename = d_data.fileScan(file_root)
        if len(filename) == 0:
            return
        for filepath in filename:
            logger.info('本次执行的文件为:\n{}'.format(filepath))
            cases = d_data.dataLoad('{}{}{}'.format(file_root, '/', filepath))
            if len(cases) == 0:
                continue
            try:
                if len(cases) == 1:
                    v_c = Validator(cases[0])
                    v_c.case_change = False
                    logger.info('本次执行的case名称为:\n{}'.format(v_c.name))
                    logger.info('本次执行的case的url为:\n{}'.format(v_c.url))
                    logger.info('本次执行的case的method为:\n{}'.format(v_c.method))
                    logger.info('本次执行的case的data为:\n{}'.format(v_c.post_data))
                    req = RequestsResource()
                    res = req.request_helper(v_c.method, v_c.url, v_c.post_data, v_c.headers)
                    logger.info('本次执行的case的response status_code为:\n{}'.format(res.status_code))
                    if res.status_code > 200:
                        logger.error('statuscode not equal 200, actual is {}. case is \n {}'.format(res.status_code, v_c))
                        raise
                    if "application/json" in res.headers['content-type'] or 'application/json' in res.headers['Content-Type']:
                        res_data = req.json_helper(res)
                        logger.info('本次执行的case的response headers为:\n{}'.format(res.headers))
                        logger.info('本次执行的case的response data为:\n{}'.format(res_data))
                        v_c.schema_validate(res_data)
                    if v_c.case_change:
                        cases[0]['schema'] = v_c.schema
                    if v_c.case_change:
                        d_data.dataStore(cases, '{}{}{}'.format(file_root, '/', filepath))
                else:
                    logger.error('case length is too long, set one case only...')
                    raise
            except Exception as e:
                logging.error('diff run has exception. {}'.format(e))


if __name__ == '__main__':

    obj = DiffRun()
    obj.run()

