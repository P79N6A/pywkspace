#!/usr/bin/env python
# coding: utf-8
# Copyright © 2017 头条网 All Rights Reserved.
# duanlingling (duanlingling@bytedance.com)

import logging
import requests
import json

logger = logging.getLogger('util.requestHandler')

class RequestsResource():

    def request_helper(self, method = 'GET', url = None, params = None, headers = None):
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'


        if method.upper() == 'POST':
            response = requests.post(url, data=params, headers=headers)
        else:
            response = requests.get(url)

        return response

    def json_helper(self, response):

        res_headers = response.headers

        if 'application/json' in res_headers['content-type'] or 'application/json' in res_headers['Content-Type']:
            return json.loads(response.content)
        else:
            return response.content
