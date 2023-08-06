"""Nornir Akamai global management tasks.

Allows to get secrets from Secret Server.
"""
from typing import Optional

from nornir.core.task import Result, Task

from nornir_akamai.plugins.connections.akamai import akamai_rest_client

GLOBAL_TRAFFIC_MANAGEMENT_ENDPOINT = "/config-gtm/v1"


def get_datacenter(task: Task, domain_name: str, datacenter_id: int) -> Result:
    url = f"https://{task.host.hostname}{GLOBAL_TRAFFIC_MANAGEMENT_ENDPOINT}/domains/{domain_name}/datacenters/{datacenter_id}"
    resp = akamai_rest_client(task).get(url)

    return Result(host=task.host, result=resp.json())


def get_status(task: Task, domain_name: str) -> Result:
    url = f"https://{task.host.hostname}{GLOBAL_TRAFFIC_MANAGEMENT_ENDPOINT}/domains/{domain_name}/status/current"
    resp = akamai_rest_client(task).get(url)

    return Result(host=task.host, result=resp.json())


def list_datacenters(task: Task, domain_name: str) -> Result:
    url = f"https://{task.host.hostname}{GLOBAL_TRAFFIC_MANAGEMENT_ENDPOINT}/domains/{domain_name}/datacenters"
    resp = akamai_rest_client(task).get(url)

    return Result(host=task.host, result=resp.json())


def list_domains(task: Task) -> Result:
    url = f"https://{task.host.hostname}{GLOBAL_TRAFFIC_MANAGEMENT_ENDPOINT}/domains"
    resp = akamai_rest_client(task).get(url)

    return Result(host=task.host, result=resp.json())


def list_properties(task: Task, domain_name: str) -> Result:
    url = f"https://{task.host.hostname}{GLOBAL_TRAFFIC_MANAGEMENT_ENDPOINT}/domains/{domain_name}/properties"
    resp = akamai_rest_client(task).get(url)

    return Result(host=task.host, result=resp.json())