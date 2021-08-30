import pytest as pytest

from didcomm.common.resolvers import ResolversConfig
from didcomm.message import Attachment, Message, AttachmentDataJson
from didcomm.pack_encrypted import pack_encrypted
from didcomm.unpack import unpack
from tests.common.example_resolvers import ExampleSecretsResolver, ExampleDIDResolver

ALICE_DID = "did:example:alice"
BOB_DID = "did:example:bob"

resolvers_config = ResolversConfig(
    secrets_resolver=ExampleSecretsResolver(), did_resolver=ExampleDIDResolver()
)


@pytest.mark.asyncio
async def test_demo_attachments():
    # ALICE
    attachment = Attachment(
        id="123",
        data=AttachmentDataJson(json={"foo": "bar"}),
        description="foo attachment",
        media_type="application/didcomm-encrypted+json",
    )
    message = Message(
        body={"aaa": 1, "bbb": 2},
        id="1234567890",
        type="my-protocol/1.0",
        frm=ALICE_DID,
        to=[BOB_DID],
        created_time=1516269022,
        expires_time=1516385931,
        attachments=[attachment],
    )
    pack_result = await pack_encrypted(
        message=message, frm=ALICE_DID, to=BOB_DID, resolvers_config=resolvers_config
    )
    packed_msg = pack_result.packed_msg
    print(f"Sending ${packed_msg} to ${pack_result.service_metadata.service_endpoint}")

    # BOB
    unpack_result = await unpack(packed_msg, resolvers_config=resolvers_config)
    print(f"Got ${unpack_result.message}")
