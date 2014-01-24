#!/usr/bin/env python
# -*- charset: utf-8 -*-

from jubatest import *

from common import APITestBase, StandaloneTestBase, DistributedTestBase

class AnomalyAPITestBase(APITestBase):
    @classmethod
    def service(cls):
        return ANOMALY

    def test_clear_row(self):
        d = self.types.datum([], [])
        result = self.cli.add(d)
        self.assertEqual(self.cli.clear_row(result.id), True)
        # TODO: return true when non existent id ..
        # self.assertEqual(self.cli.clear_row("non-existent-id"), False)

    def test_add(self):
        d = self.types.datum([], [])
        result = self.cli.add(d)

    def test_update(self):
        d = self.types.datum([], [])
        result = self.cli.add(d)
        d = self.types.datum([], [('val', 3.1)])
        score = self.cli.update(result.id, d)

    def test_calc_score(self):
        d = self.types.datum([], [('val', 1.1)])
        result = self.cli.add(d)
        d = self.types.datum([], [('val', 3.1)])
        score = self.cli.calc_score(d)

    def test_get_all_rows(self):
        self.cli.get_all_rows()

    def test_usecase_basic(self): # TODO
        self.test_add()
        self.test_clear()

        self.test_update()
        self.test_clear()

        self.test_clear_row()
        self.test_clear()

        self.test_calc_score()
        self.test_clear()

        self.test_get_all_rows()
        self.test_clear()

        self.test_save_load()

        # commons
        self.test_get_config()
        self.test_get_status()
        self.test_get_client()

class AnomalyAPIStandaloneTest(StandaloneTestBase, AnomalyAPITestBase, JubaTestCase):   pass
class AnomalyAPIDistributedTest(DistributedTestBase, AnomalyAPITestBase, JubaTestCase): pass
