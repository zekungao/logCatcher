#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
from src.metric import Metric


class Block(Metric):
    def __init__(self, key: str, expand=0, id=0):
        self.metrics = {}
        pattern = f'.*{key}'
        pattern += max(1, expand) * '.*\n'
        super(Block, self).__init__(pattern, id)

    def add(self, name, metric: Metric):
        metric.compile(self.content)
        self.metrics[name] = metric
        return self.metrics[name]

    def to_dict(self):
        dict = {}
        for key, value in self.metrics.items():
            if isinstance(value, Metric):
                dict[key] = value.to_dict()
            else:
                dict[key] = value
        return dict


class Catcher(Block):
    def __init__(self, src=""):
        self.metrics = {}
        self.content = src

    def read(self, file: str):
        with open(file, 'r') as f:
            self.content = f.read()

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def write(self, path):
        with open(path, 'w') as f:
            f.write(self.to_json())
