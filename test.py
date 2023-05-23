#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import unittest
import filecmp
from src.catcher import Catcher, Block, Metric, FloatMetric


class Unittest(unittest.TestCase):
    test_src = "mytest key=foo \"not integer\n x555 format value: \n-5.123"

    def test_metric(self):
        m = []
        m.append(Metric(r'x\d+', 0))
        m.append(Metric(r'key=[a-z]+', 0))
        m.append(FloatMetric(-1))
        m.append(FloatMetric(2))
        for ele in m:
            ele.init(self.test_src)
        self.assertEqual(m[0].content, 'x555')
        self.assertEqual(m[1].content, 'key=foo')
        self.assertEqual(m[2].content, "-5.123")
        self.assertEqual(m[3].content, "not found")

    def test_block(self):
        b = Block("key", 2)
        b.init(self.test_src)
        self.assertEqual(b.content,
                         'mytest key=foo \"not integer\n x555 format value: \n')

    def test_to_dict(self):
        c = Catcher(self.test_src)
        b = c.add("test", Block("key"))
        b.add("key", Metric(r'(?<=key=)[a-z]+', 0))
        dict = c.to_dict()
        self.assertEqual(dict["test"]["key"], "foo")


class Regressions(unittest.TestCase):
    def test_primetime_global_timing_max(self):
        case_file = "./test/PrimeTime.report.example.global.max"
        c = Catcher()
        c.read(case_file)
        b = c.add("Setup", Block("Setup violations", 8))
        b1 = b.add("wns", Block("WNS", 1))
        b1.add("total", FloatMetric(0))
        b1.add("reg2reg", FloatMetric(1))
        b1.add("in2reg", FloatMetric(2))
        b1.add("reg2out", FloatMetric(3))
        b1.add("in2out", FloatMetric(4))

        b2 = b.add("tns", Block("TNS", 1))
        b2.add("total", FloatMetric(0))
        b2.add("reg2reg", FloatMetric(1))
        b2.add("in2reg", FloatMetric(2))
        b2.add("reg2out", FloatMetric(3))
        b2.add("in2out", FloatMetric(4))

        golden = f'{case_file}.ok'
        revise = f'{case_file}.json'
        c.write(revise)
        self.assertTrue(filecmp.cmp(golden, revise))


if __name__ == '__main__':
    unittest.main()
