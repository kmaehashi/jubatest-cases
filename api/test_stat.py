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
        self.cli.push(self.name, "sum", 1.0)
        self.cli.push(self.name, "sum", 2.0)
        self.cli.push(self.name, "sum", 3.0)
        self.cli.push(self.name, "sum", 4.0)
        self.cli.push(self.name, "sum", 5.0)
        self.assertEqual(self.cli.sum(self.name, "sum"), 15.0)

    def test_stddev(self):
        self.cli.push(self.name, "stddev", 1.0)
        self.cli.push(self.name, "stddev", 2.0)
        self.cli.push(self.name, "stddev", 3.0)
        self.cli.push(self.name, "stddev", 4.0)
        self.cli.push(self.name, "stddev", 5.0)
        self.assertEqual(self.cli.stddev(self.name, "stddev"), sqrt(2.0))

    def test_max(self):
        self.cli.push(self.name, "max", 1.0)
        self.cli.push(self.name, "max", 2.0)
        self.cli.push(self.name, "max", 3.0)
        self.cli.push(self.name, "max", 4.0)
        self.cli.push(self.name, "max", 5.0)
        self.assertEqual(self.cli.max(self.name, "max"), 5.0)

    def test_min(self):
        self.cli.push(self.name, "min", 1.0)
        self.cli.push(self.name, "min", 2.0)
        self.cli.push(self.name, "min", 3.0)
        self.cli.push(self.name, "min", 4.0)
        self.cli.push(self.name, "min", 5.0)
        self.assertEqual(self.cli.min(self.name, "min"), 1.0)

    def test_entropy(self):
        self.cli.push(self.name, "entropy", 1.0)
        self.cli.push(self.name, "entropy", 2.0)
        self.cli.push(self.name, "entropy", 3.0)
        self.cli.push(self.name, "entropy", 4.0)
        self.cli.push(self.name, "entropy", 5.0)
        self.assertEqual(self.cli.entropy(self.name, "entropy"), 0.0)

    def test_moment(self):
        self.cli.push(self.name, "moment", 1.0)
        self.cli.push(self.name, "moment", 2.0)
        self.cli.push(self.name, "moment", 3.0)
        self.cli.push(self.name, "moment", 4.0)
        self.cli.push(self.name, "moment", 5.0)
        self.assertEqual(self.cli.moment(self.name, "moment", 1, 1.0), 2.0)

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
