from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, Optional

from didcomm.common.resolvers import ResolversConfig
from didcomm.common.types import JSON, DID_OR_DID_URL, JSON_OBJ
from didcomm.message import MessageRequiredHeaders, MessageOptionalHeaders, Message


@dataclass
class ForwardBody:
    next: DID_OR_DID_URL


@dataclass
class ForwardMessage(MessageOptionalHeaders, MessageRequiredHeaders, ForwardBody):
    type: str = "https://didcomm.org/routing/2.0/forward"


@dataclass
class ForwardResult:
    forward_msg: ForwardMessage
    forwarded_msg: JSON


async def wrap_in_forward(
    packed_msg: Union[JSON_OBJ, JSON],
    routing_key_ids: List[DID_OR_DID_URL],
    forward_headers: Optional[MessageOptionalHeaders] = None,
    resolvers_config: Optional[ResolversConfig] = None,
) -> JSON:
    """
    Wraps the given packed DIDComm message in Forward messages for every routing key.

    :param packed_msg: the message to be wrapped in Forward messages
    :param routing_key_ids: a list of routing key IDs or DIDs
    :param forward_headers: optional headers for Forward message
    :param resolvers_config: Optional resolvers that can override a default resolvers registered by
                             `register_default_secrets_resolver` and `register_default_did_resolver`

    :raises DIDDocNotResolvedError: If a DID can not be resolved to a DID Doc.
    :raises DIDUrlNotFoundError: If a DID URL (for example a key ID) is not found within a DID Doc
    :raises SecretNotFoundError: If there is no secret for the given DID or DID URL (key ID)

    :return: a top-level packed Forward message as JSON string
    """
    return ""


async def unpack_forward(
    packed_msg: JSON, resolvers_config: Optional[ResolversConfig] = None
) -> ForwardResult:
    """
    Can be called by a Mediator who expects a Forward message to be unpacked

    :param packed_msg: a Forward message as JSON string to be unpacked
    :param resolvers_config: Optional resolvers that can override a default resolvers registered by
                             'register_default_secrets_resolver' and 'register_default_did_resolver'

    :raises DIDDocNotResolvedError: If a DID can not be resolved to a DID Doc.
    :raises DIDUrlNotFoundError: If a DID URL (for example a key ID) is not found within a DID Doc
    :raises SecretNotFoundError: If there is no secret for the given DID or DID URL (key ID)
    :raises MalformedMessageError: if the message is invalid (can not be decrypted, signature is invalid, the plaintext is invalid, etc.)
    :raises UnsatisfiedConstraintError: if UnpackOpts expect the message to be packed in a particular way (for example encrypted and signed),
                                        but the message is not

    :return: Forward plaintext
    """
    return ForwardResult(forward_msg=ForwardMessage(next="", id=""), forwarded_msg="")


def parse_forward(message: Message) -> ForwardResult:
    """
    Convert the given message into a Forward message.

    :raises MalformedMessageError: if unpacked plaintext is not a Forward message

    :param message: the message to be converted
    :return: a Forward message instance
    """
    return ForwardResult(forward_msg=ForwardMessage(next="", id=""), forwarded_msg="")


def is_forward(message: Message) -> bool:
    """
    A helper method to check if the given message is a Forward message.

    :param message: the message to be checked
    :return: True if the plaintext is a valid Forward message and false otherwise
    """
    return True
