import pytest as pytest

from didcomm.did_doc.did_resolver import register_default_did_resolver, DIDResolverChain
from didcomm.pack import pack
from didcomm.plaintext import Plaintext
from didcomm.protocols.forward.forward import unpack_forward, wrap_in_forward
from didcomm.secrets.secrets_resolver import register_default_secrets_resolver
from didcomm.unpack import unpack
from tests.common.interfaces_test import TestSecretsResolver, TestDIDResolver

ALICE_DID = "did:example:alice"
BOB_DID = "did:example:bob"


@pytest.mark.asyncio
async def test_demo_forward():
    register_default_did_resolver(
        DIDResolverChain([TestDIDResolver()])
    )
    register_default_secrets_resolver(TestSecretsResolver())

    # ALICE
    plaintext = Plaintext(body={"aaa": 1, "bbb": 2}, id="1234567890", type="my-protocol/1.0",
                          frm=ALICE_DID, to=[BOB_DID],
                          created_time=1516269022, expires_time=1516385931,
                          typ="application/didcomm-plain+json")
    pack_result = await pack(plaintext=plaintext)
    print(f"Sending ${pack_result.packed_msg} to ${pack_result.service_endpoint}")

    # BOB MEDIATOR
    forward_bob = await unpack_forward(packed_msg=pack_result.packed_msg)
    print(f"Sending ${forward_bob.forwarded_msg} to Bob")

    # BOB
    unpack_result_bob = await unpack(forward_bob.forwarded_msg)
    print(unpack_result_bob.plaintext)


@pytest.mark.asyncio
async def test_demo_mediators_unknown_to_sender():
    register_default_did_resolver(
        DIDResolverChain([TestDIDResolver()])
    )
    register_default_secrets_resolver(TestSecretsResolver())

    # ALICE
    plaintext = Plaintext(body={"aaa": 1, "bbb": 2}, id="1234567890", type="my-protocol/1.0",
                          frm=ALICE_DID, to=[BOB_DID],
                          created_time=1516269022, expires_time=1516385931,
                          typ="application/didcomm-plain+json")
    pack_result = await pack(plaintext=plaintext)
    print(f"Sending ${pack_result.packed_msg} to ${pack_result.service_endpoint}")

    # BOB MEDIATOR 1: re-wrap to a new mediator
    forward_bob_1 = await unpack_forward(pack_result.packed_msg)
    forward_bob_2 = await wrap_in_forward(packed_msg=forward_bob_1.forwarded_msg,
                                          routing_keys=["mediator2-routing-key"])
    print(f"Sending ${forward_bob_2} to Bob Mediator 2")

    # BOB MEDIATOR 2
    forward_bob = await unpack_forward(forward_bob_2)
    print(f"Sending ${forward_bob.forwarded_msg} to Bob")

    # BOB
    unpack_result_bob = await unpack(forward_bob.forwarded_msg)
    print(unpack_result_bob.plaintext)
