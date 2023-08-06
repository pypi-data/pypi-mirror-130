from typing import List
from requests.auth import AuthBase
from .base_client import BaseServiceClient
from ..exceptions import ServiceException


class CollectionsClient(BaseServiceClient):
    """
    A Client for a DNAStack Collections instance

    :param url: The url of the Collections service
    :param auth:
    """

    def __init__(self, url: str, auth: AuthBase = None):
        super().__init__(
            url=url,
            service_type="collections",
            auth=auth,
        )

    def list_collections(self) -> List[dict]:
        """
        Return a list of collections available at the Collections url

        :return: A list of collection metadata
        """
        return self.client.get(self.url).json()

    def list_tables(self, collection_name: str) -> List[dict]:
        """
        Returns a list of table within the specified collection

        :param collection_name: The name of the collection
        :return: A dict of table metadata of the tables in the collection
        """
        collection_tables_url = self.url + f"{collection_name}/data-connect/tables"
        return self.client.get(collection_tables_url).json()

    def query(self, collection_name: str, q: str) -> dict:
        """
        Execute a SQL query against a Collection

        :param collection_name: The name of the collection
        :param q: The query to be executed
        :return: A dict object of query results
        """
        collection_query_url = self.url + f"{collection_name}/data-connect/search"
        res = self.client.post(collection_query_url, json={"query": q})

        if not res.ok:

            error_msg = f"Unable to query collection"
            if res.status_code == 401:
                error_msg += ": The request was not authenticated"
            elif res.status_code == 403:
                error_msg += ": Access Denied"
            else:
                error_json = res.json()
                if "errors" in error_json:
                    error_msg += f' ({error_json["errors"][0]["title"]})'

            raise ServiceException(
                msg=error_msg, url=self.url, service_type="collections"
            )

        results = res.json()

        return results["data"]
