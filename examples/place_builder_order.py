import os

from dotenv import load_dotenv
from py_builder_signing_sdk.config import BuilderApiKeyCreds, BuilderConfig

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs
from py_clob_client.order_builder.constants import BUY

load_dotenv()


def main():
    host = os.getenv("CLOB_API_URL", "https://clob.polymarket.com")
    key = os.getenv("PK")
    funder = os.getenv("FUNDER")
    creds = ApiCreds(
        api_key=os.getenv("CLOB_API_KEY"),
        api_secret=os.getenv("CLOB_SECRET"),
        api_passphrase=os.getenv("CLOB_PASS_PHRASE"),
    )
    builder_config = BuilderConfig(
        local_builder_creds=BuilderApiKeyCreds(
            key=os.getenv("BUILDER_API_KEY"),
            secret=os.getenv("BUILDER_SECRET"),
            passphrase=os.getenv("BUILDER_PASS_PHRASE"),
        )
    )
    client = ClobClient(
        host,
        key=key,
        chain_id=137,
        creds=creds,
        funder=funder,
        signature_type=2,
        builder_config=builder_config,
    )

    order_args = OrderArgs(
        price=0.99,
        size=2,
        side=BUY,
        token_id="13327731700723336605330749197217196859843130399253783486932713131362146632673",
    )
    signed_order = client.create_order(order_args)
    resp = client.post_order(signed_order)
    print(resp)
    print("Done!")


main()
