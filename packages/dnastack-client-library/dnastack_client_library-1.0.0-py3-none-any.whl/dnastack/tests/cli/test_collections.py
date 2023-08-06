import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli

from .base import BaseCliTestCase
from .utils import assert_has_property, set_cli_config, clear_config
from .. import *


class TestCliCollectionsCommand(BaseCliTestCase):
    def setUp(self):
        clear_config()
        self.collections_url = TEST_COLLECTIONS_URI
        set_cli_config(self.runner, "collections.url", self.collections_url)

    def test_collections_list(self):
        result = self.assertCommand(["collections", "list"], json_output=True)
        for item in result:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "id")

    def test_collections_tables_list(self):
        result = self.assertCommand(
            ["collections", "tables", "list", TEST_COLLECTION_NAME], json_output=True
        )
        for item in result:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "data_model")
            assert_has_property(self, item["data_model"], "$ref")

    def test_collections_tables_list_bad_collection(self):
        result = self.assertCommand(
            ["collections", "tables", "list", "bad-collection"], json_output=True
        )
        self.assertEqual(len(result), 0)

    def test_collections_query(self):
        result = self.assertCommand(
            ["collections", "query", TEST_COLLECTION_NAME, TEST_COLLECTION_QUERY],
            json_output=True,
        )

        self.assertGreater(len(result), 0)

        for item in result:
            assert_has_property(self, item, "start_position")
            assert_has_property(self, item, "sequence_accession")

    def test_collections_query_bad_query(self):
        result = self.assertCommand(
            [
                "collections",
                "query",
                TEST_COLLECTION_NAME,
                "SELECT badfield FROM badtable",
            ],
            exit_code=1,
        )
        # make sure it gives the collection name and url
        self.assertIn(TEST_COLLECTIONS_URI, result)

    def test_collections_query_bad_collection(self):
        result = self.assertCommand(
            ["collections", "query", "badcollection", "SELECT * FROM table"],
            exit_code=1,
        )

        # make sure it gives the collection name and url
        self.assertIn(TEST_COLLECTIONS_URI, result)
