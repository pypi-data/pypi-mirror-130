from typing import Iterator
import requests
from requests import HTTPError, Request
from search_python_client.search import SearchClient

from .base_client import BaseServiceClient
from ..auth import TokenStoreAuth
from ..exceptions import ServiceException


class DataConnectClient(BaseServiceClient):
    """
    A Client for the GA4GH Data Connect standard


    """

    def __init__(self, url: str, auth: TokenStoreAuth):
        super().__init__(url=url)
        self.auth = auth

    @property
    def _client(self) -> SearchClient:
        """
        Get a SearchClient instance, which is authorized if the service has an access token

        :return: a :class:`SearchClient` instance
        """
        if self.auth:
            req = Request(url=self.url)
            return SearchClient(self.url, wallet=self.auth.get_access_token(req))
        else:
            return SearchClient(self.url)

    def query(self, q: str) -> Iterator:
        """
        Run an SQL query against a Data Connect instance

        :param q: The SQL query to be executed
        :return: The formatted result of the SQL query
        """

        try:
            results = self._client.search_table(q)
            return results
        except HTTPError as h:
            res = h.response
            error_msg = f"The query was unsuccessful"
            if res.status_code == 401:
                error_msg += ": The request was not authenticated"
            elif res.status_code == 403:
                error_msg += ": Access Denied"
            else:
                error_json = res.json()
                if "errors" in error_json:
                    error_msg += f' ({error_json["errors"][0]["title"]})'

            raise ServiceException(
                url=self.url,
                msg=error_msg,
            )

    def list_tables(self) -> Iterator:
        """
        Return the list of tables available at the Data Connect instance

        :return: A dict of available tables' metadata.
        """

        try:
            tables = self._client.get_table_list()
        except HTTPError as e:
            error_res = requests.get(e.response.url)
            error_msg = f"The server returned HTTP error code {e.response.status_code}"
            if error_res.ok:
                error_json = error_res.json()
                if "errors" in error_json:
                    error_msg += f' ({error_json["errors"][0]["title"]})'

            raise ServiceException(
                url=self.url,
                msg=error_msg,
            )

        return tables

    def get_table(self, table_name: str) -> dict:
        """
        Get table metadata for a specific table

        :param table_name: The name of the table
        :return: A dict of table metadata.
        """

        try:
            table_info = self._client.get_table_info(table_name)
        except HTTPError as e:
            error_res = requests.get(e.response.url)
            error_msg = f"The server returned HTTP error code {e.response.status_code}"
            if error_res.ok:
                error_json = error_res.json()
                if "errors" in error_json:
                    error_msg += f' ({error_json["errors"][0]["title"]})'

            raise ServiceException(
                url=self.url,
                msg=error_msg,
            )

        # formatting response to remove unnecessary fields
        results = table_info.to_dict()
        results["name"] = table_info["name"]["$id"]
        results["description"] = table_info["description"]["$id"]

        return results
