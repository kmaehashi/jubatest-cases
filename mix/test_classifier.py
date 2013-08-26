#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from jubatest import *
from jubatest.log import LogLevel

from common import MixOperationTestBase

class MixOperationClassifierTestBase(MixOperationTestBase):
    @classmethod
    def engine(cls):
        return CLASSIFIER

    def servers(self):
        raise NotImplementedError

    def do_train(self, server, key, weight):
        d = self.server1.types.datum([], [(str(key), float(weight))])
        server.get_client().train(self.cluster.name, [('label1', d)])

    def do_classify_assertion(self, key, score):
        for cli in map(lambda s: s.get_client(), self.servers()):
            d = self.server1.types.datum([], [(key, 1.0)])
            result = cli.classify(self.cluster.name, [d])
            self.assertEquals(1, len(result))
            self.assertEquals(1, len(result[0]))
            self.assertEquals('label1', result[0][0].label)
            self.assertEquals(score, result[0][0].score)

    def do_test(self, func):
        (result, timeLeft) = self.assertRunsWithin(3, func)
        sleep(4) # wait for mix to complete
        for cond in result:
            self.do_classify_assertion(cond[0], cond[1])

    def dataset1_1(self):
        count = len(self.servers())
        self.do_train(self.server1, 'a', 3.0)
        return [('a', (3.0 / count))]

    def dataset1_2(self):
        count = len(self.servers())
        self.do_train(self.server1, 'a', 3.0)
        self.do_train(self.server2, 'a', 6.0)
        return [('a', ((3.0 + 6.0) / count))]

    def dataset1_3(self):
        count = len(self.servers())
        self.do_train(self.server1, 'a', 3.0)
        self.do_train(self.server2, 'a', 6.0)
        self.do_train(self.server3, 'a', 9.0)
        return [('a', ((3.0 + 6.0 + 9.0) / count))]

    def dataset2_1(self):
        count = len(self.servers())
        self.do_train(self.server1, 'a', 3.0)
        return [('a', 3.0 / count)]

    def dataset2_2(self):
        count = len(self.servers())
        self.do_train(self.server1, 'a', 3.0)
        self.do_train(self.server2, 'b', 6.0)
        return [('a', 3.0 / count), ('b', 6.0 / count)]

    def dataset2_3(self):
        count = len(self.servers())
        self.do_train(self.server1, 'a', 3.0)
        self.do_train(self.server2, 'b', 6.0)
        self.do_train(self.server3, 'c', 9.0)
        return [('a', 3.0 / count), ('b', 6.0 / count), ('c', 9.0 / count)]

class MixOperationClassifierTest_2_Servers(JubaTestCase, MixOperationClassifierTestBase):
    def servers(self):
        return [self.server1, self.server2]

    def setUp(self):
        for server in self.servers():
            server.start()

    def tearDown(self):
        for server in self.servers():
            server.stop()

    def test_update_request_1(self):
        self.do_test(self.dataset1_1)

    def test_update_request_2(self):
        self.do_test(self.dataset1_2)

    def test_noupdate_request_1(self):
        self.do_test(self.dataset2_1)

    def test_noupdate_request_2(self):
        self.do_test(self.dataset2_2)

class MixOperationClassifierTest_3_Servers(MixOperationClassifierTest_2_Servers):
    def servers(self):
        return [self.server1, self.server2, self.server3]

    def test_update_request_3(self):
        self.do_test(self.dataset1_3)

    def test_noupdate_request_3(self):
        self.do_test(self.dataset2_3)
