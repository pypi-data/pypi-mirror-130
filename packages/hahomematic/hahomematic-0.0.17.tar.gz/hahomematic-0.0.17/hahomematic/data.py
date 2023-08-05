"""
Module to store data required for operation.
"""
from __future__ import annotations

import hahomematic.central_unit as hm_central

# {instance_name, central_unit}
INSTANCES: dict[str, hm_central.CentralUnit] = {}


def get_client_by_interface_id(interface_id):
    """Return client by interface_id"""
    for central in INSTANCES.values():
        if client := central.clients.get(interface_id):
            return client
