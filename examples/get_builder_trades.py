import os
from collections import Counter
from pprint import pprint

from dotenv import load_dotenv
from py_builder_signing_sdk.config import BuilderApiKeyCreds, BuilderConfig

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, TradeParams
from py_clob_client.constants import POLYGON

load_dotenv()


def print_statistics(trades):
    """Print statistics about builder trades."""
    if not trades:
        print("No trades found.")
        return

    total_trades = len(trades)

    # Calculate totals
    total_volume_usdc = sum(float(trade.get("sizeUsdc", 0)) for trade in trades)
    total_fees_usdc = sum(float(trade.get("feeUsdc", 0)) for trade in trades)

    # Calculate average price
    prices = [float(trade.get("price", 0)) for trade in trades if trade.get("price")]
    avg_price = sum(prices) / len(prices) if prices else 0

    # Breakdown by side
    sides = Counter(trade.get("side", "UNKNOWN") for trade in trades)

    # Breakdown by trade type
    trade_types = Counter(trade.get("tradeType", "UNKNOWN") for trade in trades)

    # Breakdown by status
    statuses = Counter(trade.get("status", "UNKNOWN") for trade in trades)

    # Breakdown by outcome
    outcomes = Counter(trade.get("outcome", "UNKNOWN") for trade in trades)

    # Unique markets
    unique_markets = len(set(trade.get("market", "") for trade in trades))

    # Date range
    dates = [trade.get("createdAt", "") for trade in trades if trade.get("createdAt")]
    if dates:
        dates.sort()
        earliest = dates[0]
        latest = dates[-1]
    else:
        earliest = latest = "N/A"

    # Volume by side
    buy_volume = sum(
        float(trade.get("sizeUsdc", 0))
        for trade in trades
        if trade.get("side") == "BUY"
    )
    sell_volume = sum(
        float(trade.get("sizeUsdc", 0))
        for trade in trades
        if trade.get("side") == "SELL"
    )

    # Fees by side
    buy_fees = sum(
        float(trade.get("feeUsdc", 0)) for trade in trades if trade.get("side") == "BUY"
    )
    sell_fees = sum(
        float(trade.get("feeUsdc", 0))
        for trade in trades
        if trade.get("side") == "SELL"
    )

    print("\n" + "=" * 60)
    print("BUILDER TRADES STATISTICS")
    print("=" * 60)
    print(f"\nTotal Trades: {total_trades}")
    print(f"Unique Markets: {unique_markets}")
    print(f"\nDate Range:")
    print(f"  Earliest: {earliest}")
    print(f"  Latest: {latest}")

    print(f"\nVolume Statistics:")
    print(f"  Total Volume (USDC): ${total_volume_usdc:,.2f}")
    print(f"  Buy Volume (USDC): ${buy_volume:,.2f}")
    print(f"  Sell Volume (USDC): ${sell_volume:,.2f}")
    print(f"  Average Price: {avg_price:.6f}")

    print(f"\nFee Statistics:")
    print(f"  Total Fees (USDC): ${total_fees_usdc:,.2f}")
    print(f"  Buy Fees (USDC): ${buy_fees:,.2f}")
    print(f"  Sell Fees (USDC): ${sell_fees:,.2f}")
    if total_volume_usdc > 0:
        fee_percentage = (total_fees_usdc / total_volume_usdc) * 100
        print(f"  Fee Rate: {fee_percentage:.4f}%")

    print(f"\nSide Breakdown:")
    for side, count in sides.most_common():
        percentage = (count / total_trades) * 100
        print(f"  {side}: {count} ({percentage:.1f}%)")

    print(f"\nTrade Type Breakdown:")
    for trade_type, count in trade_types.most_common():
        percentage = (count / total_trades) * 100
        print(f"  {trade_type}: {count} ({percentage:.1f}%)")

    print(f"\nStatus Breakdown:")
    for status, count in statuses.most_common():
        percentage = (count / total_trades) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")

    print(f"\nOutcome Breakdown:")
    for outcome, count in outcomes.most_common():
        percentage = (count / total_trades) * 100
        print(f"  {outcome}: {count} ({percentage:.1f}%)")

    print("=" * 60 + "\n")


def main():
    host = os.getenv("CLOB_API_URL", "https://clob.polymarket.com")
    key = os.getenv("PK")
    creds = ApiCreds(
        api_key=os.getenv("CLOB_API_KEY"),
        api_secret=os.getenv("CLOB_SECRET"),
        api_passphrase=os.getenv("CLOB_PASS_PHRASE"),
    )
    chain_id = POLYGON
    builder_config = BuilderConfig(
        local_builder_creds=BuilderApiKeyCreds(
            key=os.getenv("BUILDER_API_KEY"),
            secret=os.getenv("BUILDER_SECRET"),
            passphrase=os.getenv("BUILDER_PASS_PHRASE"),
        )
    )

    client = ClobClient(
        host, key=key, chain_id=chain_id, creds=creds, builder_config=builder_config
    )

    resp = client.get_builder_trades()

    # Print statistics
    print_statistics(resp)

    # Optionally print raw data (commented out to reduce output)
    # pprint(resp)
    print("Done!")


main()
