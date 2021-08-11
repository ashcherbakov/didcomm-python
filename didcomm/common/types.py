from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Union, List

JSON_DATA = Union[Dict[str, Any], List[Any]]
JSON = str
JWK = JSON
JWT = JSON
JWS = JSON
DID = str
DID_URL = str
DID_OR_DID_URL = Union[DID, DID_URL]


@dataclass(frozen=True)
class ServiceMetadata:
    id: str
    service_endpoint: str
