from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from didcomm.common.types import DID_URL


@dataclass
class Secret:
    """
    A secret (private key) abstraction.

    Attributes:
        kid (str): a key ID identifying a secret (private key).
        Must have the same value, as key ID ('id' field) of the corresponding method in DID Doc containing a public key.

        type (str): secret (private key) type.
        Must have the same value, as type ('type' field) of the corresponding method in DID Doc containing a public key.

        value (str): value of the secret (private key) as a string.
        The value is type-specific, and has the same format as the corresponding public key value from the DID Doc.
        For example, for 'JsonWebKey2020' type it will be a JWK JSON string.
        For 'X25519KeyAgreementKey2019' type it will be a base58-encoded string.
    """
    kid: DID_URL
    type: str
    value: str


class SecretsResolver(ABC):
    """Resolves secrets such as private keys to be used for signing and encryption."""

    @abstractmethod
    async def get_key(self, kid: DID_URL) -> Optional[Secret]:
        """
        Finds d private key identified by the given key ID.

        :param kid: the key ID identifying a private key
        :return: a private key or None of there is no key for the given key ID
        """
        pass

    @abstractmethod
    async def get_keys(self, kids: List[DID_URL]) -> List[DID_URL]:
        """
        Find all private keys that have one of the given key IDs.
        Return keys only for key IDs for which a key is present.

        :param kids: the key IDs find private keys for
        :return: a possible empty list of all private keys that have one of the given keyIDs.
        """
        pass
