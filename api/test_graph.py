#!/usr/bin/env python
# -*- charset: utf-8 -*-

from jubatest import *

from common import APITestBase, StandaloneTestBase, DistributedTestBase

class GraphAPITestBase(APITestBase):
    @classmethod
    def service(cls):
        return GRAPH

    def test_node_info(self):
        edge_query = [["a", "b"], ["c", "d"], ["e", "f"]]
        node_query = [["0", "1"], ["2", "3"]]
        p = self.types.preset_query(edge_query, node_query)
        in_edges = [0, 0]
        out_edges = [0, 0]
        self.types.node(p, in_edges, out_edges)

    def test_create_node(self):
        nid = self.cli.create_node(self.name)
        self.assertEqual(str(int(nid)), nid)

    def test_remove_node(self):
        nid = self.cli.create_node(self.name)
        self.assertEqual(self.cli.remove_node(self.name, nid), True)

    def test_update_node(self):
        nid = self.cli.create_node(self.name)
        prop = {"key1":"val1", "key2":"val2"}
        self.assertEqual(self.cli.update_node(self.name, nid, prop), True)

    def test_create_edge(self):
        src = self.cli.create_node(self.name)
        tgt = self.cli.create_node(self.name)
        prop = {"key1":"val1", "key2":"val2"}
        ei = self.types.edge(prop, src, tgt)
        eid = self.cli.create_edge(self.name, tgt, ei)

    # TODO lacks some APIs

    def test_usecase_basic(self): # TODO
        self.test_create_node()
        self.test_clear()

        self.test_update_node()
        self.test_clear()

        self.test_remove_node()
        self.test_clear()

        self.test_node_info()
        self.test_clear()

        self.test_create_edge()
        self.test_clear()

        self.test_save_load()

        # commons
        self.test_get_config()
        self.test_get_status()
        self.test_get_client()

class GraphAPIStandaloneTest(StandaloneTestBase, GraphAPITestBase, JubaTestCase):   pass
class GraphAPIDistributedTest(DistributedTestBase, GraphAPITestBase, JubaTestCase): pass
