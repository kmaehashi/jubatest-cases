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
        (row_id, score) = self.cli.add(self.name, d)
        self.assertEqual(self.cli.clear_row(self.name, row_id), True)
        # TODO: return true when non existent id ..
        # self.assertEqual(self.cli.clear_row(self.name, "non-existent-id"), False)

    def test_add(self):
        d = self.types.datum([], [])
        (row_id, score) = self.cli.add(self.name, d)

    def test_update(self):
        d = self.types.datum([], [])
        (row_id, score) = self.cli.add(self.name, d)
        d = self.types.datum([], [('val', 3.1)])
        score = self.cli.update(self.name, row_id, d)

    def test_calc_score(self):
        d = self.types.datum([], [('val', 1.1)])
        (row_id, score) = self.cli.add(self.name, d)
        d = self.types.datum([], [('val', 3.1)])
        score = self.cli.calc_score(self.name, d)

    def test_get_all_rows(self):
        self.cli.get_all_rows(self.name)

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
