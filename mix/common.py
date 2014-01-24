#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from jubatest import *

class MixOperationTestBase(object):
    @classmethod
    def setUpCluster(cls, env):
        engine = cls.engine()
        config = default_config(engine)

        if cls.use_idf():
            config['converter']['string_rules'][0]['global_weight'] = 'idf'

        cls.node0 = env.get_node(0)
        cls.cluster = env.cluster(engine, config)

        # server1 always become MIX master
        cls.server1 = env.server(cls.node0, cls.cluster, [('--interval_sec', 3)])
        cls.server2 = env.server(cls.node0, cls.cluster, [('--interval_sec', 0)])
        cls.server3 = env.server(cls.node0, cls.cluster, [('--interval_sec', 0)])

    @classmethod
    def engine(cls):
        # please override in subclasses
        # return CLASSIFIER
        raise NotImplementedError

    @classmethod
    def use_idf(cls):
        # please override in subclasses
        return False
