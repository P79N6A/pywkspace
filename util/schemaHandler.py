#!/usr/bin/env python
# coding: utf-8
# Copyright © 2017 头条网 All Rights Reserved.
# duanlingling (duanlingling@bytedance.com)
import json

import genson

class SchemaHandler():

    def json_to_schema(self, data):
        schema = genson.Schema()
        schema.add_object(data)
        schema = schema.to_json()
        if isinstance(schema, str):
            schema = json.loads(schema)
        return schema

