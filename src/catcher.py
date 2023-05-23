#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import re


class Metric:
    def __init__(self, pattern: str, index=0):
        self.pattern = pattern
        self.index = index
        self.content = "not found"

    def init(self, src: str):
        catch = re.findall(self.pattern, src)
        if len(catch) > max(0, self.index):
            self.content = catch[self.index]

    def _to_dict(self):
        return self.content


class FloatMetric(Metric):
    def __init__(self, index=0):
        super(FloatMetric, self).__init__(r'-?\d+.?\d+', index)


class Block(Metric):
    def __init__(self, key: str, expand=0, id=0):
        self.metrics = {}
        pattern = f'.*{key}'
        pattern += max(1, expand) * '.*\n'
        super(Block, self).__init__(pattern, id)

    def _add(self, name, metric: Metric):
        metric.init(self.content)
        self.metrics[name] = metric
        return self.metrics[name]

    def _to_dict(self):
        dict = {}
        for key, value in self.metrics.items():
            if isinstance(value, Metric):
                dict[key] = value._to_dict()
            else:
                dict[key] = value
        return dict


class Catcher(Block):
    def __init__(self, src=""):
        self.metrics = {}
        self.content = src
    
    def _read(self, file: str):
        with open(file, 'r') as f:
            self.content = f.read()

    def _to_json(self):
        return json.dumps(self._to_dict(), sort_keys=True, indent=4)

    def _write(self, path):
        with open(path, 'w') as f:
            f.write(self._to_json())
