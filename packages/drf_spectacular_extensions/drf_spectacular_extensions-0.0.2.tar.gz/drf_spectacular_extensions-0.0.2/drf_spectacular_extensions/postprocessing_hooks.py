from typing import Optional

from drf_spectacular.generators import SchemaGenerator
from rest_framework.request import Request


def add_servers(
    result: dict,
    generator: SchemaGenerator,
    request: Optional[Request],
    public: bool,
) -> dict:
    if request:
        result["servers"] = [{"url": f"{request.scheme}://{request.get_host()}/"}]
    return result
