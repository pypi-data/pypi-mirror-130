from enum import Enum
from typing import Optional, Any

import requests
from requests import Session, Request
from requests.auth import AuthBase

from ..auth import TokenStoreAuth
from ..exceptions import ServiceTypeNotFoundError, ServiceException


class BaseServiceClient:
    """
    The base class for all DNAStack Clients

    :param parent: The parent :class:`PublisherClient` instance of the client. If a parent is not defined, the
    service client will create its own :class:`AuthClient` for authorization
    :param url: The url of the service to be configured
    :param **kwargs: Additional keyword arguments to be passed to the :class:`AuthClient` if necessary
    """

    def __init__(self, auth: AuthBase = None, url: str = None, **kwargs):
        self.__auth = auth

        self.__client = requests.Session()
        self.__client.auth = self.__auth

        self.url = url

    def __del__(self):
        self.__client.close()

    @property
    def auth(self):
        return self.__auth

    @auth.setter
    def auth(self, auth: AuthBase):
        self.__auth = auth

        if hasattr(self, "client"):
            self.__client.auth = auth

    @property
    def client(self) -> Session:
        return self.__client

    def authorize(self):
        if isinstance(self.__auth, TokenStoreAuth):
            self.__auth.authorize(Request(url=self.url))
        else:
            raise AttributeError(
                "The service auth must be a TokenStoreAuth in order to authorize"
            )
