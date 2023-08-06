"""Nornir Akamai connections."""

from nornir_akamai.plugins.connections.akamai import (
    CONNECTION_NAME,
    AkamaiRestClient,
    akamai_rest_client,
)

__all__ = (
    "CONNECTION_NAME",
    "AkamaiRestClient",
    "akamai_rest_client",
)