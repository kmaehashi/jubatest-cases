#!/usr/bin/env python
# -*- charset: utf-8 -*-

from jubatest import *

from common import APITestBase, StandaloneTestBase, DistributedTestBase

class ClassifierAPITestBase(APITestBase):
    @classmethod
    def service(cls):
        return CLASSIFIER

    def make_datum(self):
        string_values = [["key1", "val1"], ["key2", "val2"]]
        num_values = [["key1", 1.0], ["key2", 2.0]]
        return self.types.datum(string_values, num_values)

    def test_train(self):
        d = self.make_datum()
        self.assertEqual(1, self.cli.train([["label", d]]))

    def test_classify(self):
        d = self.make_datum()
        self.assertEqual([[]], self.cli.classify([d]))

    def test_basic_usecase(self):
        client = self.cli

        d1 = self.types.datum([("d1", "abc")], [])
        d2 = self.types.datum([("d2", "def")], [])
        d3 = self.types.datum([("d3", "ghi")], [])

        # update
        result = client.train([("label1", d1), ("label2", d2)])
        self.assertEqual(2, result)

        # analysis
        def _analysis(label, d):
            result = client.classify([d])
            self.assertEqual(1, len(result))
            self.assertEqual(1, len(result[0]))
            self.assertEqual(label, result[0][0].label)
            self.assertTrue(0 < result[0][0].score)
        _analysis("label1", d1)

        # save
        result = client.save('model')
        self.assertTrue(result)

        # clear
        result = client.clear()
        self.assertTrue(result)

        # analysis
        result = client.classify([d1])
        self.assertEqual(1, len(result))
        self.assertEqual(0, len(result[0]))

        # load
        result = client.load('model')
        self.assertTrue(result)

        # analysis
        _analysis("label2", d2)

        # update
        result = client.train([("label3", d3)])
        self.assertEqual(1, result)

        # analysis
        _analysis("label3", d3)

        # commons
        self.test_get_config()
        self.test_get_status()
        self.test_get_client()

class ClassifierAPIStandaloneTest(StandaloneTestBase, ClassifierAPITestBase, JubaTestCase):   pass
class ClassifierAPIDistributedTest(DistributedTestBase, ClassifierAPITestBase, JubaTestCase): pass
