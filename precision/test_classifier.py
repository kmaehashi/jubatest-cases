#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from jubatest import *
from jubatest.unit import JubaSkipTest

class ClassifierPrecisionTestBase(object):
    def test(self):
        # train
        for (label, message) in self.entries_in('train.dat'):
            d = self.types.datum([["message", message]], [])
            self.cli.train(self.name, [(label, d)])

        # classify
        (match, unmatch) = (0, 0)
        for (label, message) in self.entries_in('test.dat'):
            d = self.types.datum([["message", message]], [])
            results = self.cli.classify(self.name, [d])[0]
            results.sort(key=lambda e: e.score, reverse=True)
            if 0 < len(results) and results[0].label == label:
                match += 1
            else:
                unmatch += 1
        self.attach_record({'ok': match, 'fail': unmatch})

    def entries_in(self, path):
        result = []
        with open(self.JUBATUS_TUTORIAL_DIR + '/' + path) as msgs_list:
            for line in msgs_list:
                (label, msg_file_path) = line[:-1].split(',')
                with open(self.JUBATUS_TUTORIAL_DIR + '/' + msg_file_path) as msg_file:
                    msg_data = msg_file.read()
                result += [(label, msg_data)]
        return result

    @classmethod
    def setUpTutorialDirectory(cls, env):
        cls.JUBATUS_TUTORIAL_DIR = env.get_param('JUBATUS_TUTORIAL_DIR')
        if not cls.JUBATUS_TUTORIAL_DIR:
            raise JubaSkipTest("JUBATUS_TUTORIAL_DIR parameter is not set")

    @classmethod
    def get_config(cls):
        with open(cls.JUBATUS_TUTORIAL_DIR + '/config.json') as f:
            return json.loads(f.read())

class ClassifierPrecisionStandaloneTest(JubaTestCase, ClassifierPrecisionTestBase):
    @classmethod
    def setUpCluster(cls, env):
        cls.setUpTutorialDirectory(env)
        cls.server1 = env.server_standalone(env.get_node(0), CLASSIFIER, cls.get_config())
        cls.name = ''

    def setUp(self):
        self.server1.start()
        self.cli = self.server1.get_client()
        self.types = self.server1.types

    def tearDown(self):
        self.server1.stop()

class ClassifierPrecisionDistributedTest(JubaTestCase, ClassifierPrecisionTestBase):
    @classmethod
    def setUpCluster(cls, env):
        cls.setUpTutorialDirectory(env)
        cls.node0 = env.get_node(0)
        cls.cluster = env.cluster(CLASSIFIER, cls.get_config())
        cls.server1 = env.server(cls.node0, cls.cluster)
        cls.server2 = env.server(cls.node0, cls.cluster)
        cls.keeper1 = env.keeper(cls.node0, CLASSIFIER)
        cls.name = cls.cluster.name

    def setUp(self):
        self.keeper1.start()
        self.cluster.start()
        self.cli = self.keeper1.get_client()
        self.types = self.keeper1.types

    def tearDown(self):
        self.keeper1.stop()
        self.cluster.stop()
