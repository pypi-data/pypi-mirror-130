import os

from requests.auth import AuthBase
from . import *
from typing import Union, List, Any
from .base_client import BaseServiceClient
from ..auth import TokenStoreAuth
from ..exceptions import ServiceTypeNotFoundError


class PublisherClient:
    """
    A Client for DNAStack suite of products (Data Connect, WES, Collections, etc.)


    :param dataconnect_url: The url for the Data Connect instance
    :param collections_url: The url for the Collections instance
    :param wes_url: The url for the Workflow Execution Service (WES) instance
    """

    def __init__(
        self,
        dataconnect_url: str = None,
        collections_url: str = None,
        wes_url: str = None,
        auth: AuthBase = None,
    ):
        self.auth = auth
        self.__services = []

        # Since search_python_client strictly uses bearer auth, we only create it if its an instance of that
        if isinstance(self.auth, TokenStoreAuth):
            self.__files = FilesClient(self.auth)
            self.__dataconnect = DataConnectClient(url=dataconnect_url, auth=self.auth)
        else:
            self.__files = FilesClient(None)
            self.__dataconnect = DataConnectClient(url=dataconnect_url, auth=None)

        self.__collections = CollectionsClient(url=collections_url, auth=self.auth)
        self.__wes = WesClient(url=wes_url, auth=auth)

    @property
    def dataconnect(self):
        return self.__dataconnect

    @property
    def collections(self):
        return self.__collections

    @property
    def wes(self):
        return self.__wes

    @property
    def files(self):
        return self.__files

    def get_services(self) -> List[BaseServiceClient]:
        """
        Return all configured services.

        :return: List of all configured clients (dataconnect, collections, wes)
        """
        return [self.dataconnect, self.collections, self.wes]

    def load(self, urls: Union[str, List[str]]) -> Any:
        """
        Return the raw output of one or more DRS resources

        :param urls: One or a list of DRS urls (drs://...)
        :return: The raw output of the specified DRS resource
        """
        if isinstance(urls, str):
            urls = [urls]

        download_content = []

        self.files.download_files(
            urls=urls,
            display_progress_bar=False,
            out=download_content,
        )
        return download_content

    def download(
        self,
        urls: Union[str, List[str]],
        output_dir: str = os.getcwd(),
        display_progress_bar: bool = False,
    ) -> None:
        """
        Download one or more DRS resources from the specified urls

        :param urls: One or a list of DRS urls (drs://...)
        :param output_dir: The directory to output the downloaded files to.
        :param display_progress_bar: Display the progress of the downloads. This is False by default
        :return:
        """
        if isinstance(urls, str):
            urls = [urls]

        self.files.download_files(
            urls=urls,
            output_dir=output_dir,
            display_progress_bar=display_progress_bar,
        )
