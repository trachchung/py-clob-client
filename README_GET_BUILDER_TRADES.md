source .venv/bin/activate

uv pip install py_clob_client

.env
PK=
CLOB_API_URL=https://clob.polymarket.com

uv run examples/create_api_key.py
ApiCreds(api_key=, api_secret=, api_passphrase=)

uv run examples/get_builder_trades.py
