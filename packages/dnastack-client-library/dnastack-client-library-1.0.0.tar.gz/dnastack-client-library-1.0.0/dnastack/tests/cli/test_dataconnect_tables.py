import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli

from .base import BaseCliTestCase
from .utils import *
from .. import *


class TestCliDataConnectTablesCommand(BaseCliTestCase):
    def setUp(self):
        self.data_connect_url = TEST_DATA_CONNECT_URI

        clear_config()
        set_cli_config(self.runner, "data_connect.url", self.data_connect_url)
        set_auth_params_for_service(
            self.runner,
            service="dataconnect",
            auth_params=TEST_AUTH_PARAMS["publisher"],
        )
        set_cli_config(
            self.runner,
            f"data_connect.auth.client.scope",
            TEST_AUTH_SCOPES["publisher"],
        )
        set_cli_config(
            self.runner,
            f"data_connect.auth.refresh_token",
            TEST_WALLET_REFRESH_TOKEN["publisher"],
        )

    def test_tables_list(self):
        result = self.assertCommand(["dataconnect", "tables", "list"], json_output=True)
        for item in result:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "data_model")
            assert_has_property(self, item["data_model"], "$ref")

    def test_tables_get_table(self):
        table_info_object = self.assertCommand(
            ["dataconnect", "tables", "get", TEST_DATA_CONNECT_VARIANTS_TABLE],
            json_output=True,
        )

        assert_has_property(self, table_info_object, "name")
        assert_has_property(self, table_info_object, "description")
        assert_has_property(self, table_info_object, "data_model")
        assert_has_property(self, table_info_object["data_model"], "$id")
        assert_has_property(self, table_info_object["data_model"], "$schema")
        assert_has_property(self, table_info_object["data_model"], "description")

        for property in table_info_object["data_model"]["properties"]:
            assert_has_property(
                self, table_info_object["data_model"]["properties"][property], "format"
            )
            assert_has_property(
                self, table_info_object["data_model"]["properties"][property], "type"
            )
            assert_has_property(
                self,
                table_info_object["data_model"]["properties"][property],
                "$comment",
            )

    def test_tables_get_table_does_not_exist(self):
        self.assertCommand(
            ["dataconnect", "tables", "get", "some table name"], exit_code=1
        )
