import typing

from pycspr.api_v1.get_rpc_schema import execute as get_rpc_schema
from pycspr.types import NodeConnectionInfo



def execute(connection_info: NodeConnectionInfo) -> typing.List[str]:
    """Returns set of JSON-RPC endpoints.

    :param connection_info: Information required to connect to a node.
    :returns: A list of all supported RPC endpoints.

    """
    schema = get_rpc_schema(connection_info)

    return sorted([i["name"] for i in schema["methods"]])
