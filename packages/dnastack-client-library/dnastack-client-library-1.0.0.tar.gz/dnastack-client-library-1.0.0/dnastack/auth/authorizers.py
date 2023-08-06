from datetime import datetime
from typing import AnyStr, Dict, Any
from requests import Request
from requests.auth import AuthBase
from .oauth_client import OAuthClient, DEFAULT_AUTH_CLIENT
from .token_store import TokenStore, TokenStore, get_audience_from_url
from .utils import login_refresh_token, login_personal_access_token, login_device_code
from ..exceptions import AuthException


class TokenStoreAuth(AuthBase):
    """
    An AuthBase implementation that caches generated tokens.
    """

    def __init__(self):
        self.token_store = TokenStore()
        super().__init__()

    def __call__(self, req: Request) -> Request:
        """
        This function is called by the requests library to modify client requests as they are sent.
        In our case we get an access token then pass it along to

        :param req: The outbound :class:`requests.Request`
        :return: A modified request with the Authorization header set to a Bearer token
        """
        access_token = self.get_access_token(req)

        req.headers["Authorization"] = f"Bearer {access_token}"
        return req

    def get_access_token(self, req: Request) -> AnyStr:
        """
        Obtain an OAuth access token to attach to a request. If it is in token storage it will return the cached token
        Otherwise it will look to authorize the request.

        :param req: The request we look to generate an access token for.
        :return: The Bearer token authorizing the request
        """
        access_token = self.token_store.get_token(req)

        if access_token:
            return access_token
        else:
            return self.authorize(req)

    def authorize(self, req: Request, **kwargs) -> AnyStr:
        """
        Authorize a request by generating then storing an OAuth access token

        :param req: The requests.Request to authorize.
        :param kwargs: Any additional keyword arguments to be passed to the generate_access_token function
        :return: The OAuth access token authorizing the request
        :raise: AuthException if there is no url to authorize or it cannot generate an access token
        """
        if not req.url:
            raise AuthException("There is no url to authorize")

        token_entry = self.generate_access_token(req, **kwargs)
        access_token = None
        if token_entry:
            access_token = token_entry.get("access_token")

        if access_token:
            self.token_store.set_token(token_entry, req)
            return access_token
        else:
            raise AuthException(url=req.url, msg="Could not retrieve a token")

    def generate_access_token(self, req: Request, **kwargs) -> AnyStr:
        """
        Generate a new OAuth Access Token for a specific request

        :param req: The :class:`requests.Request` to authorize
        :param kwargs: Any additional keyword arguments used in generating a
        :return:
        """
        raise NotImplementedError(
            "The Base TokenStoreAuth cannot generate its own access token"
        )


class PersonalAccessTokenAuth(TokenStoreAuth):
    """
    A Service Client authorization method using a DNAStack Personal Access Token (PAT)

    :param email: The email to authorize the user
    :param personal_access_token: The Personal Access Token (PAT) used to authorize the user
    :param oauth_client: The :class:`OAuthClient` to authorize the user with.
    """

    def __init__(
        self,
        email: AnyStr,
        personal_access_token: AnyStr,
        oauth_client: OAuthClient = DEFAULT_AUTH_CLIENT,
    ):
        self.email = email
        self.personal_access_token = personal_access_token
        self.oauth_client = oauth_client
        super().__init__()

    def generate_access_token(self, req: Request, **kwargs) -> Dict[AnyStr, Any]:
        oauth_response = login_personal_access_token(
            email=self.email,
            personal_access_token=self.personal_access_token,
            oauth_client=self.oauth_client,
            audience=[get_audience_from_url(req.url)],
        )
        if oauth_response.get("access_token"):
            oauth_response["issuer"] = self.oauth_client.base_url
            return oauth_response
        else:
            raise AuthException(
                url=req.url,
                msg="Unable to retrieve access token using Personal Access Token",
            )


class DeviceCodeAuth(TokenStoreAuth):
    """
    A Service Client authorization method using the OAuth Device Code method

    :param oauth_client: The :class:`OAuthClient` to authorize the user with.
    """

    def __init__(
        self,
        oauth_client: OAuthClient = DEFAULT_AUTH_CLIENT,
    ):
        self.oauth_client = oauth_client
        super().__init__()

    def generate_access_token(self, req: Request, **kwargs) -> Dict[AnyStr, Any]:
        oauth_response = login_device_code(
            oauth_client=self.oauth_client,
            audience=[get_audience_from_url(req.url)],
            **kwargs,
        )
        if oauth_response.get("access_token"):
            oauth_response["issuer"] = self.oauth_client.base_url
            return oauth_response
        else:
            raise AuthException(
                url=req.url, msg="Unable to retrieve access token using Device Code"
            )


class RefreshTokenAuth(TokenStoreAuth):
    """
    A Service Client authorization method using the OAuth Refresh Token method

    :param refresh_token: An OAuth Refresh Token to authorize the user
    :param oauth_client: The :class:`OAuthClient` to authorize the user with.
    """

    def __init__(
        self,
        refresh_token: AnyStr,
        oauth_client: OAuthClient = DEFAULT_AUTH_CLIENT,
    ):
        self.refresh_token = refresh_token
        self.oauth_client = oauth_client
        super().__init__()

    def generate_access_token(self, req: Request, **kwargs) -> Dict[AnyStr, Any]:
        oauth_response = login_refresh_token(
            token=self.refresh_token,
            oauth_client=self.oauth_client,
        )
        if oauth_response.get("access_token"):
            oauth_response["issuer"] = self.oauth_client.base_url
            oauth_response["expiry"] = int(
                datetime.now().timestamp()
            ) + oauth_response.get("expires_in")
            return oauth_response
        else:
            raise AuthException(
                url=req.url, msg="Unable to retrieve access token using Refresh Token"
            )
