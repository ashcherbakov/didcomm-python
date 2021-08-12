from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from didcomm.common.resolvers import ResolversConfig
from didcomm.common.types import JSON, DID_OR_DID_URL
from didcomm.message import Message


async def pack_signed(message: Message,
                      sign_frm: DID_OR_DID_URL,
                      resolvers_config: Optional[ResolversConfig] = None) -> PackSignedResult:
    """
    Produces `DIDComm Signed Message`
    https://identity.foundation/didcomm-messaging/spec/#didcomm-signed-message.

    The method signs (non-repudiation added) the message keeping it unencrypted.

    Signed messages are only necessary when
        - the origin of plaintext must be provable to third parties
        - or the sender can’t be proven to the recipient by authenticated encryption because the recipient
          is not known in advance (e.g., in a broadcast scenario).

    Adding a signature when one is not needed can degrade rather than enhance security because it
    relinquishes the sender’s ability to speak off the record.

    Signing is done as follows:
        - Signing is done via the keys from the `authentication` verification relationship in the DID Doc
          for the DID to be used for signing
        - If `sign_frm` is a DID, then the first sender's `authentication` verification method is used for which
          a private key in the secrets resolver is found
        - If `sign_frm` is a key ID, then the sender's `authentication` verification method identified by the given key ID is used.

    :param message: The message to be packed into a DIDComm message
    :param sign_frm: DID or key ID the sender uses for signing.
    :param resolvers_config: Optional resolvers that can override a default resolvers registered by
                             `register_default_secrets_resolver` and `register_default_did_resolver`

    :raises DIDDocNotResolvedError: If a DID can not be resolved to a DID Doc.
    :raises DIDUrlNotFoundError: If a DID URL (for example a key ID) is not found within a DID Doc
    :raises SecretNotFoundError: If there is no secret for the given DID or DID URL (key ID)

    :return: A packed message as a JSON string.
    """
    return PackSignedResult("", "")


@dataclass(frozen=True)
class PackSignedResult:
    """
    Result of pack operation.

    Attributes:
        packed_msg (str): A packed message as a JSON string
        sign_from_kid (DID_OR_DID_URL): Identifier (DID URL) of sender key used for message signing
    """
    packed_msg: JSON
    sign_from_kid: DID_OR_DID_URL
