import os

from dotenv import load_dotenv

from py_clob_client.client import ClobClient

load_dotenv()


def main():
    host = os.getenv("CLOB_API_URL", "https://clob.polymarket.com")
    key = os.getenv("PK")

    client = ClobClient(host, key=key, chain_id=137)

    print(client.create_or_derive_api_creds())


main()
