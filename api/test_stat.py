#!/usr/bin/env python
# -*- charset: utf-8 -*-

from math import sqrt

from jubatest import *

from common import APITestBase, StandaloneTestBase, DistributedTestBase

class StatAPITestBase(APITestBase):
    @classmethod
    def service(cls):
        return STAT

    def test_sum(self):
        self.cli.push("sum", 1.0)
        self.cli.push("sum", 2.0)
        self.cli.push("sum", 3.0)
        self.cli.push("sum", 4.0)
        self.cli.push("sum", 5.0)
        self.assertEqual(self.cli.sum("sum"), 15.0)

    def test_stddev(self):
        self.cli.push("stddev", 1.0)
        self.cli.push("stddev", 2.0)
        self.cli.push("stddev", 3.0)
        self.cli.push("stddev", 4.0)
        self.cli.push("stddev", 5.0)
        self.assertEqual(self.cli.stddev("stddev"), sqrt(2.0))

    def test_max(self):
        self.cli.push("max", 1.0)
        self.cli.push("max", 2.0)
        self.cli.push("max", 3.0)
        self.cli.push("max", 4.0)
        self.cli.push("max", 5.0)
        self.assertEqual(self.cli.max("max"), 5.0)

    def test_min(self):
        self.cli.push("min", 1.0)
        self.cli.push("min", 2.0)
        self.cli.push("min", 3.0)
        self.cli.push("min", 4.0)
        self.cli.push("min", 5.0)
        self.assertEqual(self.cli.min("min"), 1.0)

    def test_entropy(self):
        self.cli.push("entropy", 1.0)
        self.cli.push("entropy", 2.0)
        self.cli.push("entropy", 3.0)
        self.cli.push("entropy", 4.0)
        self.cli.push("entropy", 5.0)
        self.assertEqual(self.cli.entropy("entropy"), 0.0)

    def test_moment(self):
        self.cli.push("moment", 1.0)
        self.cli.push("moment", 2.0)
        self.cli.push("moment", 3.0)
        self.cli.push("moment", 4.0)
        self.cli.push("moment", 5.0)
        self.assertEqual(self.cli.moment("moment", 1, 1.0), 2.0)

    def test_usecase_basic(self): # TODO
        self.test_sum()
        self.test_clear()

        self.test_stddev()
        self.test_clear()

        self.test_max()
        self.test_clear()

        self.test_min()
        self.test_clear()

        self.test_entropy()
        self.test_clear()

        self.test_moment()
        self.test_clear()

        self.test_save_load()

        # commons
        self.test_get_config()
        self.test_get_status()
        self.test_get_client()

class StatAPIStandaloneTest(StandaloneTestBase, StatAPITestBase, JubaTestCase):   pass
class StatAPIDistributedTest(DistributedTestBase, StatAPITestBase, JubaTestCase): pass
