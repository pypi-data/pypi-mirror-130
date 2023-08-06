"""Nornir Akamai connection plugin.

Allows to interact with Akamai appliances.
"""

from typing import Any, Dict, Optional

import requests
import urllib3
from nornir.core import Task
from nornir.core.configuration import Config
from requests import Response
from requests.adapters import HTTPAdapter
from requests_toolbelt.utils import dump
from urllib3.util import Retry

from akamai.edgegrid import EdgeGridAuth

urllib3.disable_warnings()

CONNECTION_NAME = "akamai"
DEFAULT_RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
DEFAULT_TIMEOUT = 5  # seconds


class _TimeoutHTTPAdapter(HTTPAdapter):
    """Custom `Transport Adapter` with a default timeout.

    This class allows to set a default timeout for all HTTP calls.
    """

    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)


def _assert_status_hook(response: Response, *args, **kwargs) -> None:
    response.raise_for_status()


def _logging_hook(response: Response, *args, **kwargs) -> None:
    data = dump.dump_all(response)
    print(data.decode("utf-8"))


class AkamaiRestClient:
    """Connection plugin for Akamai appliances.

    This plugin allows to make calls to an Akamai REST API.

    Authentication is handled automatically.
    """

    def open(  # noqa A003
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        """Opens a connection to Akamai.

        Args:
            hostname (Optional[str]): The hostname of the device.
            username (Optional[str]): The username used to access the device.
            password (Optional[str]): The password used to access the device.
            port (Optional[int]): The service port.
            platform (Optional[str]): The device family platform.
            extras (Optional[Dict[str, Any]): The extra variables.
            configuration (Optional[Config]): The configuration.
        """
        session = requests.Session()
        session.auth = EdgeGridAuth(
            client_token=extras.get("client_token", ""),
            client_secret=extras.get("client_secret", ""),
            access_token=extras.get("access_token", ""),
        )

        session.verify = extras.get("validate_certs", False)

        hooks = [_assert_status_hook]
        if extras.get("debug"):
            hooks.append(_logging_hook)
        session.hooks["response"] = hooks

        kwargs = {
            "max_retries": DEFAULT_RETRY_STRATEGY,
            "timeout": extras.get("timeout", None),
        }
        adapter = _TimeoutHTTPAdapter(
            **{k: v for k, v in kwargs.items() if v is not None}
        )
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        # Set the host. This is used by the close method to delete the token.
        self.host = hostname

        self.connection = session

    def close(self) -> None:
        """Closes the connection."""
        self.connection.close()


def akamai_rest_client(task: Task) -> AkamaiRestClient:
    """Returns a REST client to interact with Akamai's REST API.

    Args:
        task (Task): The Nornir task.

    Returns:
        AkamaiRestClient: The Akamai REST client.
    """
    return task.host.get_connection(CONNECTION_NAME, task.nornir.config)