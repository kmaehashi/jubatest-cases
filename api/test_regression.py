#!/usr/bin/env python
# -*- charset: utf-8 -*-

from jubatest import *

from common import APITestBase, StandaloneTestBase, DistributedTestBase

class RegressionAPITestBase(APITestBase):
    @classmethod
    def service(cls):
        return REGRESSION

    def make_datum(self):
        string_values = [["key1", "val1"], ["key2", "val2"]]
        num_values = [["key1", 1.0], ["key2", 2.0]]
        return self.types.datum(string_values, num_values)

    def test_train(self):
        d = self.make_datum()
        self.assertEqual(1, self.cli.train(self.name, [[1.0, d]]))

    def test_estimate(self):
        d = self.make_datum()
        self.assertEqual([0.0], self.cli.estimate(self.name, [d]))

    def test_basic_usecase(self):
        client = self.cli

        d1 = self.types.datum([("d1", "abc")], [])
        d2 = self.types.datum([("d2", "def")], [])
        d3 = self.types.datum([("d3", "ghi")], [])

        # update
        result = client.train(self.name, [(1.0, d1), (1.0, d2)])
        self.assertEqual(2, result)

        # analysis
        def _analysis(score, d):
            result = client.estimate(self.name, [d])
            self.assertEqual(1, len(result))
            self.assertEqual(score, result[0])
        _analysis(1.0, d1)

        # save
        result = client.save(self.name, 'model')
        self.assertTrue(result)

        # clear
        result = client.clear(self.name)
        self.assertTrue(result)

        # analysis
        _analysis(0.0, d1)

        # load
        result = client.load(self.name, 'model')
        self.assertTrue(result)

        # analysis
        _analysis(1.0, d2)

        # update
        result = client.train(self.name, [(1.0, d3)])
        self.assertEqual(1, result)

        # analysis
        _analysis(1.0, d3)

        # commons
        self.test_get_config()
        self.test_get_status()
        self.test_get_client()

class RegressionAPIStandaloneTest(StandaloneTestBase, RegressionAPITestBase, JubaTestCase):   pass
class RegressionAPIDistributedTest(DistributedTestBase, RegressionAPITestBase, JubaTestCase): pass
