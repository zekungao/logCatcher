#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re


class Metric:
    def __init__(self, pattern: str, index=0):
        self.pattern = pattern
        self.content = "not found"
        self.index = index

    def compile(self, src: str):
        catch = re.findall(self.pattern, src)
        if len(catch) > max(0, self.index):
            self.content = catch[self.index]

    def to_dict(self):
        return self.content


# template to catch float variable
# which is fine if you use it to catch integer
class FloatMetric(Metric):
    def __init__(self, index=0):
        super(FloatMetric, self).__init__(r'-?\d+.?\d+', index)


class IntegerMetric(Metric):
    def __init__(self, index=0):
        super(IntegerMetric, self).__init__(r'-?\d+', index)


# enum
# to support some fix content pattern, e.g. week days
# it is necessary to add enum pattern one by one
# case sensitive and supports escaping <careful!>
class EnumMetric(Metric):
    def __init__(self, enum: list, index=0,):
        super(EnumMetric, self).__init__('', index)
        self.enum = enum
        self.compile_pattern()

    def compile_pattern(self):
        pat = ""
        for ele in self.enum:
            pat = f'{pat}(?<![a-zA-Z0-9]){ele}(?![a-zA-Z0-9])|'
        self.pattern = pat.strip('|')

    def set_divider(self, div: str):
        self.start_div = div
        self.end_div = div
