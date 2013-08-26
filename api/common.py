#!/usr/bin/env python
# -*- charset: utf-8 -*-

from jubatest import *

import json
import msgpackrpc

class APITestBase():
    @classmethod
    def service(cls):
        raise NotImplementedError

    @classmethod
    def config(cls):
        return default_config(cls.service())

    @classmethod
    def get_client(cls):
        return cls.default_route.get_client()

    @property
    def types(cls):
        return cls.default_route.types

    #########################################
    # Test for Common API methods
    #########################################

    def test_save_load(self):
        self.assertTrue(self.cli.save(self.name, 'test'))
        self.assertTrue(self.cli.load(self.name, 'test'))

    def test_clear(self):
        self.assertTrue(self.cli.clear(self.name))

    def test_get_config(self):
        config = self.cli.get_config(self.name)
        self.assertEqual(json.dumps(json.loads(config), sort_keys=True), json.dumps(self.config(), sort_keys=True))

    def test_get_status(self):
        status = self.cli.get_status(self.name)
        self.assertTrue(0 < len(status))

    def test_get_client(self):
        self.assertTrue(isinstance(self.cli.get_client(), msgpackrpc.client.Client))

class StandaloneTestBase():
    @classmethod
    def setUpCluster(cls, env):
        cls.node0 = env.get_node(0)
        cls.server1 = env.server_standalone(cls.node0, cls.service(), cls.config())
        cls.default_route = cls.server1
        cls.name = ''

    def setUp(self):
        self.server1.start()
        self.cli = self.get_client()

    def tearDown(self):
        self.server1.stop()

class DistributedTestBase():
    @classmethod
    def setUpCluster(cls, env):
        cls.node0 = env.get_node(0)
        cls.cluster = env.cluster(cls.service(), cls.config())
        cls.keeper1 = env.keeper(cls.node0, cls.service())
        cls.server1 = env.server(cls.node0, cls.cluster)
        cls.default_route = cls.keeper1
        cls.name = cls.cluster.name

    def setUp(self):
        self.cluster.start()
        self.keeper1.start()
        self.cli = self.get_client()

    def tearDown(self):
        self.cluster.stop()
        self.keeper1.stop()

class DistributedMultiServerTestBase(DistributedTestBase):
    @classmethod
    def setUpCluster(cls, env):
        super(DistributedMultiServerTestBase, self).setUpCluster(env)
        cls.server2 = env.server(cls.node0, cls.cluster)
