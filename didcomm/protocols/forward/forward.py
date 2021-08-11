from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, Optional

from didcomm.common.resolvers import ResolversConfig
from didcomm.common.types import JSON_DATA, JSON, DID_OR_DID_URL
from didcomm.plaintext import PlaintextRequiredHeaders, PlaintextOptionalHeaders, Plaintext


@dataclass
class ForwardBody:
    next: DID_OR_DID_URL
    forwarded_msg: JSON


@dataclass
class ForwardPlaintext(PlaintextOptionalHeaders, PlaintextRequiredHeaders, ForwardBody):
    type: str = "https://didcomm.org/routing/2.0/forward"


async def wrap_in_forward(packed_msg: Union[JSON_DATA, JSON], routing_key_ids: List[DID_OR_DID_URL],
                          forward_headers: Optional[PlaintextOptionalHeaders] = None,
                          resolvers_config: Optional[ResolversConfig] = None) -> JSON:
    """
    Wraps the given packed message in Forward messages for every routing key.

    :param packed_msg: the message to be wrapped in Forward messages
    :param routing_key_ids: a list of routing key IDs or DIDs
    :param forward_headers: optional headers for Forward message
    :param resolvers_config: Optional resolvers that can override a default resolvers registered by
                             `register_default_secrets_resolver` and `register_default_did_resolver`

    :raises DIDNotResolvedError: If a DID or DID URL (key ID) can not be resolved or not found
    :raises SecretNotResolvedError: If there is no secret for the given DID or DID URL (key ID)

    :return: a top-level packed Forward message as JSON string
    """
    return ""


async def unpack_forward(packed_msg: JSON,
                         resolvers_config: Optional[ResolversConfig] = None) -> ForwardPlaintext:
    """
    Can be called by a Mediator who expects a Forward message to be unpacked

    :param packed_msg: a Forward message as JSON string to be unpacked
    :param resolvers_config: Optional resolvers that can override a default resolvers registered by
                             'register_default_secrets_resolver' and 'register_default_did_resolver'

    :raises DIDNotResolvedError: If a DID or DID URL (key ID) can not be resolved or not found
    :raises SecretNotResolvedError: If there is no secret for the given DID or DID URL (key ID)
    :raises MalformedMessageError: if the message is invalid (can not be decrypted, signature is invalid, the plaintext is invalid, etc.)
    :raises UnexpectedPackError: if UnpackOpts expect the message to be packed in a particular way (for example encrypted and signed),
                                   but the message is not

    :return: Forward plaintext
    """
    return ForwardPlaintext(
        next="",
        forwarded_msg="",
        id="", type="")


def parse_forward(plaintext: Plaintext) -> ForwardPlaintext:
    """
    Convert the given plaintext into a Forward message.

    :raises MalformedMessageError: if unpacked plaintext is not a Forward message

    :param plaintext: the plaintext message to be converted
    :return: a Forward message instance
    """
    return ForwardPlaintext(
        next="",
        forwarded_msg="",
        id="", type="")


def is_forward(plaintext: Plaintext) -> bool:
    """
    A helper method to check if the given plaintext is a Forward message.

    :param plaintext: the plaintext to be checked
    :return: True if the plaintext is a valid Forward message and false otherwise
    """
    return True
