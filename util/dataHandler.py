#!/usr/bin/env python
# coding: utf-8
# Copyright © 2017 头条网 All Rights Reserved.
# duanlingling (duanlingling@bytedance.com)

import json
import os

class DataHandler():

    def fileScan(self, filepath):
        for root, dirs, files in os.walk(filepath):
            return files

    def dataStore(self, data, filepath):
        with open(filepath, 'w') as json_file:
            json_file.write(json.dumps(data))

    def dataLoad(self, filepath):
        try:
            with open(filepath) as json_file:
                data = json.load(json_file)
                return data
        except Exception:
            return {}