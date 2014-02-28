#!/usr/bin/env python

from jubatest import *
from jubatest.log import LogLevel

class ClassifierChaosTest(JubaTestCase):
    def setUp(self):
        self.cluster.start()
        self.proxy0.start()
        self.proxy0.wait_for_servers(*self.cluster.get_servers())

    def tearDown(self):
        self.cluster.stop()
        self.proxy0.stop()

    def test_chaos(self):
        # Train data for 10 times via Proxy
        cli = self.proxy0.get_client(self.name)
        for i in range(10):
            d = self.proxy0.types.Datum({'text': 'test-' + str(i)})
            self.assertEqual(1, cli.train([('label-' + str(i), d)]))

        # Perform MIX
        self.server0.do_mix()

        # Kill server0, server1
        self.server0.kill()
        self.server1.kill()

        # Restart server0
        self.server0.start()

        # Wait for server0 to become active
        self.proxy0.wait_for_servers(self.server0)

        # Kill server2
        self.server2.kill()

        # Restart server1, server2
        self.server1.start()
        self.server2.start()

        # Wait for server[0-2] to become active
        self.proxy0.wait_for_servers(*self.cluster.get_servers())

        # Confirm that trained data is preserved on all servers
        for server in self.cluster.get_servers():
            cli = server.get_client()
            for i in range(10):
                d = server.types.Datum({'text': 'test-' + str(i)})
                result = cli.classify([d])
                self.assertEqual(1, len(result))

                # 10 labels are trained
                self.assertEqual(10, len(result[0]))

                # sort results by score
                result[0] = sorted(result[0], key=lambda x: x.score, reverse=True)

                # expected lable should be the first result
                self.assertEqual('label-' + str(i), result[0][0].label)

    @classmethod
    def setUpCluster(cls, env):
        # disable MIX for this test
        options = [('--interval_count', 0), ('--interval_sec', 0)]

        cls.node0 = env.get_node(0)
        cls.cluster = env.cluster(CLASSIFIER, default_config(CLASSIFIER))
        cls.server0 = env.server(cls.node0, cls.cluster, options)
        cls.server1 = env.server(cls.node0, cls.cluster, options)
        cls.server2 = env.server(cls.node0, cls.cluster, options)
        cls.proxy0 = env.proxy(cls.node0, CLASSIFIER)
        cls.name = cls.cluster.name
