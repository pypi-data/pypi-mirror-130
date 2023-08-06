import json
import click
import os
from typing import Any
import yaml
from requests import Request
from .auth.authorizers import TokenStore, RefreshTokenAuth, TokenStoreAuth
from .auth import DeviceCodeAuth, OAuthClient, PersonalAccessTokenAuth
from .client import PublisherClient
from .cli import *
from .cli.utils import (
    set_config_obj,
    save_config_to_file,
    get_config,
    get_service_config_key,
    set_config,
)
from .constants import (
    CLI_DIRECTORY,
    DEPRECATED_CONFIG_KEYS,
    __version__,
)


def fix_deprecated_keys(ctx: click.Context) -> None:
    """
    Change deprecated keys to their current values and save to file

    :param ctx: The context to fix the deprecated keys for
    :return:
    """
    new_keys = {}
    deprecated_keys = []

    # try to fix deprecated keys
    for key in ctx.obj.keys():
        if key in DEPRECATED_CONFIG_KEYS.keys():
            var_path = DEPRECATED_CONFIG_KEYS[key]
            # there is a new key that the value can be set to. set the analogous value to the existing one
            if var_path is not None:
                new_keys[var_path] = ctx.obj[key]
            deprecated_keys.append(key)

    # add the new keys
    for new_key, value in new_keys.items():
        var_path = new_key.split(".")
        set_config_obj(ctx.obj, var_path=var_path, value=value)

    # delete the deprecated keys
    for dep_key in deprecated_keys:
        del ctx.obj[dep_key]

    save_config_to_file(ctx)


def load_config_from_file(ctx: click.Context) -> None:
    """
    Load a config from the CLIs config file and load it into the :attr:`Context.obj` attribute of the Context

    It also fixes deprecated config keys once loaded

    :param ctx: The :class:`Context` to load config into
    """
    ctx.obj = {}

    # create the cli directory if necessary
    if not os.path.exists(CLI_DIRECTORY):
        os.mkdir(CLI_DIRECTORY)

    config_file_path = f"{CLI_DIRECTORY}/config.yaml"

    # create the config file if necessary
    if not os.path.exists(config_file_path):

        with open(config_file_path, "w+") as config_file:
            yaml.dump(ctx.obj, config_file)
            config_file.close()

    with open(config_file_path, "r+") as config_file:
        data = yaml.safe_load(config_file)
        if data:
            ctx.obj = data

    fix_deprecated_keys(ctx)


def create_publisher_client_from_config(ctx: click.Context) -> None:
    """
    Create a :class:`PublisherClient` from a configured Context object

    :param ctx: The :class:`Context` to use to create the client
    """

    tokens = get_config(ctx, "tokens", False)
    token_store = TokenStore()

    if tokens:
        tokens = json.loads(tokens)
        for token in tokens:
            token_store.set_token(token)

    publisher_auth = TokenStoreAuth()
    publisher_client = PublisherClient(
        dataconnect_url=get_config(ctx, "data_connect.url", False),
        collections_url=get_config(ctx, "collections.url", False),
        wes_url=get_config(ctx, "wes.url", False),
        auth=publisher_auth,
    )

    for service in publisher_client.get_services():

        service_auth_config = get_config(
            ctx, var_path=[get_service_config_key(service), "auth"], raise_error=False
        )

        if service_auth_config:
            service_auth = service_auth_config
            service_auth_client = service_auth.get("client")
            if service_auth_client:
                oauth_client = OAuthClient(
                    base_url=service_auth.get("url"),
                    authorization_url=service_auth.get("authorization_url"),
                    device_code_url=service_auth.get("device_code_url"),
                    token_url=service_auth.get("token_url"),
                    client_id=service_auth_client.get("id"),
                    client_secret=service_auth_client.get("secret"),
                    client_redirect_url=service_auth_client.get("redirect_url"),
                    scope=service_auth_client.get("scope"),
                )

                refresh_token = service_auth.get("refresh_token")
                # Have a preference of Refresh Token > Device Code >>>> PAT for the CLI
                if refresh_token:
                    service.auth = RefreshTokenAuth(
                        refresh_token=refresh_token,
                        oauth_client=oauth_client,
                    )
                else:
                    service.auth = DeviceCodeAuth(
                        oauth_client=oauth_client,
                    )

                if tokens:
                    for token in tokens:
                        parsed_token_url = urlparse(service.auth.oauth_client.token_url)
                        oauth_client_issuer = urlunparse(
                            (
                                parsed_token_url.scheme,
                                parsed_token_url.netloc,
                                "",
                                "",
                                "",
                                "",
                            )
                        )
                        if (
                            token.get("issuer") == oauth_client_issuer
                            and token.get("scope") == service.auth.oauth_client.scope
                        ):
                            service.auth.token_store.set_token(
                                token, Request(url=service.url)
                            )

            else:
                service.auth = None
        else:
            service.auth = None

    email = get_config(ctx, var_path=["user", "email"], raise_error=False)
    personal_access_token = get_config(
        ctx, var_path=["user", "personal_access_token"], raise_error=False
    )

    if email and personal_access_token:
        publisher_client.files.auth = PersonalAccessTokenAuth(
            email=email, personal_access_token=personal_access_token
        )
    else:
        publisher_client.files.auth = None

    ctx.obj["client"] = publisher_client


def save_publisher_client_to_config(ctx: click.Context) -> None:
    """Save the Context's configuration to a save file"""
    publisher_client = ctx.obj["client"]

    if publisher_client.auth.token_store:
        set_config(
            ctx, var_path=["tokens"], value=publisher_client.auth.token_store.tokens
        )


@click.group("dnastack")
@click.option("--debug", is_flag=True)
@click.version_option(__version__, message="%(version)s")
def dnastack(debug):
    load_config_from_file(click.get_current_context())
    create_publisher_client_from_config(click.get_current_context())
    click.get_current_context().obj["debug"] = debug


@dnastack.result_callback()
def dnastack_callback(result: Any, debug: bool):
    save_publisher_client_to_config(click.get_current_context())


@dnastack.command("version")
def get_version():
    click.echo(__version__)


dnastack.add_command(dataconnect_commands.dataconnect)
dnastack.add_command(config_commands.config)
dnastack.add_command(file_commands.files)
dnastack.add_command(auth_commands.auth)
dnastack.add_command(collections_commands.collections)
dnastack.add_command(wes_commands.wes)

if __name__ == "__main__":
    dnastack.main(prog_name="dnastack")
