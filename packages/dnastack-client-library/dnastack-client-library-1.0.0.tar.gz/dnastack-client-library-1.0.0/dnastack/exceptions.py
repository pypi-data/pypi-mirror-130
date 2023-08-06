from typing import List, Type

from dnastack.constants import DEPRECATED_CONFIG_KEYS, ACCEPTED_CONFIG_KEYS


class PublisherException(Exception):
    """
    The base class for exceptions within the Publisher python library
    """

    def __str__(self):
        return str(self.__repr__())


class ConfigException(PublisherException):
    def __init__(self, key: str):
        super().__init__()

        self.key = key


def display_keys(obj: dict, prefix: str = None) -> str:
    output = ""
    for key in sorted(obj.keys()):
        if isinstance(obj[key], dict):
            if prefix:
                output += display_keys(obj[key], prefix=f"{prefix}.{key}")
            else:
                output += display_keys(obj[key], prefix=f"{key}")
        else:
            if prefix:
                output += f"\t{prefix}.{key}\n"
            else:
                output += f"\t{key}\n"
    return output


class InvalidConfigException(ConfigException):
    def __repr__(self):
        return (
            f"The [{self.key}] is not a valid configuration key. "
            f"Accepted configuration keys:\n"
            f"{display_keys(ACCEPTED_CONFIG_KEYS)}"
        )


class NoConfigException(ConfigException):
    def __repr__(self):
        return f"There is no configuration value for key [{self.key}]"


class InvalidConfigTypeException(ConfigException):
    def __init__(self, expected: Type, actual: Type, key: str):
        super().__init__(key)
        self.expected = expected
        self.actual = actual

    def __repr__(self):
        return f"Expected type [{self.expected}] for config variable [{self.key}], got [{self.actual}]"


class DeprecatedConfigException(ConfigException):
    def __repr__(self):
        return (
            f"The [{self.key}] is deprecated. "
            f"Please use the config key [{DEPRECATED_CONFIG_KEYS[self.key]}] instead."
        )


class ServiceException(PublisherException):
    """
    An Exception that is raised for errors within Services
    """

    def __init__(self, msg: str = None, url: str = None, service_type: str = ""):
        super().__init__()

        self.msg = msg
        self.url = url
        self.service_type = service_type

    def __repr__(self):
        return f"The [{self.service_type}] service [{self.url}] failed: {self.msg}"


class ServiceTypeException(PublisherException):
    """
    An Exception that is raised for inconsistencies in service types
    """

    def __init__(self, expected_type: str, actual_type: str):
        super().__init__()

        self.expected_type = expected_type
        self.actual_type = actual_type

    def __repr__(self):
        return f"Expected service type [{self.expected_type}], got [{self.actual_type}]"


class ServiceTypeNotFoundError(PublisherException):
    def __init__(self, service_type: str):
        super().__init__()

        self.service_type = service_type

    def __repr__(self):
        return f"Could not find service type of name [{self.service_type}]"


class AuthException(ServiceException):
    pass


class LoginException(AuthException):
    def __repr__(self):
        return f"Could not log into [{self.url}]: {self.msg}"


class RefreshException(AuthException):
    def __repr__(self):
        return f"Could not refresh token for [{self.url}]: {self.msg}"


class OAuthTokenException(AuthException):
    def __repr__(self):
        return f"Could not fetch the OAuth token for [{self.url}]: {self.msg}"


class DRSException(PublisherException):
    def __init__(self, msg: str = None, url: str = None, object_id: str = None):
        self.msg = msg
        self.url = url
        self.object_id = object_id

    def __repr__(self):
        error_msg = "Failure downloading DRS object"
        if self.url:
            error_msg += f" with url [{self.url}]"
        elif self.object_id:
            error_msg += f" with object ID [{self.object_id}]"
        if self.msg:
            error_msg += f": {self.msg}"
        return error_msg


class DRSDownloadException(PublisherException):
    def __init__(self, errors: List[DRSException] = None):
        self.errors = errors

    def __repr__(self):
        error_msg = f"One or more downloads failed:\n"
        for err in self.errors:
            error_msg += f"{err}\n"
        return error_msg


class WorkflowFailedException(PublisherException):
    pass
