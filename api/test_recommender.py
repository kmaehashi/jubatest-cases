#!/usr/bin/env python
# -*- charset: utf-8 -*-

from math import sqrt

from jubatest import *

from common import APITestBase, StandaloneTestBase, DistributedTestBase

class RecommenderAPITestBase(APITestBase):
    @classmethod
    def service(cls):
        return RECOMMENDER

    def test_complete_row(self):
        self.cli.clear_row("complete_row")
        string_values = [("key1", "val1"), ("key2", "val2")]
        num_values = [("key1", 1.0), ("key2", 2.0)]
        d = self.types.datum(string_values, num_values)
        self.cli.update_row("complete_row", d)
        d1 = self.cli.complete_row_from_id("complete_row")
        d2 = self.cli.complete_row_from_datum(d)

    def test_similar_row(self):
        self.cli.clear_row("similar_row")
        string_values = [("key1", "val1"), ("key2", "val2")]
        num_values = [("key1", 1.0), ("key2", 2.0)]
        d = self.types.datum(string_values, num_values)
        self.cli.update_row("similar_row", d)
        s1 = self.cli.similar_row_from_id("similar_row", 10)
        s2 = self.cli.similar_row_from_datum(d, 10)

    def test_decode_row(self):
        self.cli.clear_row("decode_row")
        string_values = [("key1", "val1"), ("key2", "val2")]
        num_values = [("key1", 1.0), ("key2", 2.0)]
        d = self.types.datum(string_values, num_values)
        self.cli.update_row("decode_row", d)
        decoded_row = self.cli.decode_row("decode_row")
        self.assertEqual(dict(d.string_values), dict(decoded_row.string_values))
        self.assertEqual(dict(d.num_values),    dict(decoded_row.num_values))

    def test_get_row(self):
        self.cli.clear()
        string_values = [("key1", "val1"), ("key2", "val2")]
        num_values = [("key1", 1.0), ("key2", 2.0)]
        d = self.types.datum(string_values, num_values)
        self.cli.update_row("get_row", d)
        row_names = self.cli.get_all_rows()
        self.assertEqual(row_names, ["get_row"])

    def test_calc_similarity_l2norm(self):
        string_values = [("key1", "val1"), ("key2", "val2")]
        num_values = [("key1", 1.0), ("key2", 2.0)]
        d = self.types.datum(string_values, num_values)
        self.assertAlmostEqual(self.cli.calc_similarity(d, d), 1, 6)
        self.assertAlmostEqual(self.cli.calc_l2norm(d), sqrt(1*1 + 1*1+ 1*1 + 2*2), 6)

    def test_usecase_basic(self): # TODO
        self.test_complete_row()
        self.test_clear()

        self.test_similar_row()
        self.test_clear()

        self.test_decode_row()
        self.test_clear()

        self.test_get_row()
        self.test_clear()

        self.test_calc_similarity_l2norm()
        self.test_clear()

        self.test_save_load()

        # commons
        self.test_get_config()
        self.test_get_status()
        self.test_get_client()

class RecommenderAPIStandaloneTest(StandaloneTestBase, RecommenderAPITestBase, JubaTestCase):   pass
class RecommenderAPIDistributedTest(DistributedTestBase, RecommenderAPITestBase, JubaTestCase): pass
