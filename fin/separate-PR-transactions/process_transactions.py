#!/usr/bin/env python3
"""FIFO transaction matching and cutoff-period profit/loss attribution."""

import argparse
import csv
import os
import re
import sys
from collections import deque
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


ZERO = Decimal("0")
QTY_TOLERANCE = Decimal("0.000001")
MONEY_PLACES = Decimal("0.01")
LONG = 1
SHORT = -1

OPTION_SYMBOL_RE = re.compile(
    r"^-?(?P<root>[A-Z]{1,6})(?P<date>\d{6})(?P<kind>[CP])"
    r"(?P<strike>\d+(?:\.\d+)?)$",
    re.IGNORECASE,
)


def parse_date(date_str):
    """Parse an MM/DD/YYYY command-line date."""
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%Y")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: '{date_str}'. Must be MM/DD/YYYY."
        ) from exc


def parse_optional_date(date_str):
    """Parse an optional broker date, returning None for blank/invalid values."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%Y")
    except ValueError:
        return None


def parse_decimal(value):
    """Parse a broker-formatted number exactly, returning zero for a blank value."""
    cleaned = (value or "").strip().replace(",", "").replace("$", "")
    if not cleaned:
        return ZERO
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid numeric value: {value!r}") from exc


def round_money(value):
    return value.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def round_quantity(value):
    return value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def classify_asset(symbol, description="", action=""):
    """Classify options using OCC-like symbols first, then broker descriptions."""
    normalized_symbol = (symbol or "").strip().replace(" ", "")
    symbol_match = OPTION_SYMBOL_RE.fullmatch(normalized_symbol)
    if symbol_match:
        return "Put Option" if symbol_match.group("kind").upper() == "P" else "Call Option"

    text = f"{description} {action}".upper()
    if re.search(r"\bPUT\b(?:\s+OPTION)?\s*\(", text):
        return "Put Option"
    if re.search(r"\bCALL\b(?:\s+OPTION)?\s*\(", text):
        return "Call Option"
    return "Stock"


def trade_side(action):
    """Return the position direction created by an action: LONG for buy, SHORT for sell."""
    action_upper = (action or "").upper()
    if re.search(r"\b(?:BOUGHT|BUY)\b", action_upper):
        return LONG
    if re.search(r"\b(?:SOLD|SELL)\b", action_upper):
        return SHORT
    return None


def classify_trade(action, symbol="", description=""):
    """Return trade flags and asset type without relying on quantity signs."""
    action_upper = (action or "").upper()
    side = trade_side(action)
    is_trade = side is not None
    return {
        "is_trade": is_trade,
        "is_opening": is_trade and "OPENING" in action_upper,
        "is_closing": is_trade and "CLOSING" in action_upper,
        "action_side": side,
        "asset_type": classify_asset(symbol, description, action) if is_trade else "Other",
    }


def is_relevant_account(account, account_num):
    normalized = (account or "").lower().replace("-", "").replace(" ", "")
    return (
        "brok1" in normalized
        or "brok2" in normalized
        or account_num in {"X96600886", "Z34395861"}
    )


def transaction_sort_key(tx):
    """Provide a total, reproducible order when exports contain date-only timestamps."""
    settlement = tx.get("settlement_date") or datetime.max
    return (
        tx["run_date"],
        settlement,
        tx.get("file", "").casefold(),
        tx.get("source_row", 0),
    )


def load_transactions(input_dir):
    """Read and normalize relevant transactions from all CSV files."""
    transactions = []
    warnings = []

    for filename in sorted(os.listdir(input_dir)):
        if not filename.lower().endswith(".csv"):
            continue

        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source)
            header = None
            header_row = 0
            for header_row, row in enumerate(reader, start=1):
                if row and any(cell.strip() for cell in row):
                    header = [cell.strip() for cell in row]
                    break
            if header is None:
                continue

            col_map = {column: index for index, column in enumerate(header)}
            required = [
                "Run Date", "Account Number", "Action", "Symbol", "Quantity", "Amount ($)"
            ]
            missing = [column for column in required if column not in col_map]
            if missing:
                warnings.append(f"{filename}: missing columns {missing}; file skipped")
                continue

            def value(row, column):
                index = col_map.get(column)
                return row[index].strip() if index is not None and index < len(row) else ""

            for source_row, row in enumerate(reader, start=header_row + 1):
                if not row or not any(cell.strip() for cell in row):
                    continue

                account = value(row, "Account")
                account_num = value(row, "Account Number")
                if not is_relevant_account(account, account_num):
                    continue

                run_date_str = value(row, "Run Date")
                try:
                    run_date = datetime.strptime(run_date_str, "%m/%d/%Y")
                except ValueError:
                    warnings.append(
                        f"{filename}:{source_row}: invalid Run Date {run_date_str!r}; row skipped"
                    )
                    continue

                try:
                    qty = parse_decimal(value(row, "Quantity"))
                    amount = parse_decimal(value(row, "Amount ($)"))
                    price = parse_decimal(value(row, "Price ($)"))
                except ValueError as exc:
                    warnings.append(f"{filename}:{source_row}: {exc}; row skipped")
                    continue

                action = value(row, "Action")
                symbol = value(row, "Symbol")
                description = value(row, "Description")
                classification = classify_trade(action, symbol, description)
                settlement_date_str = value(row, "Settlement Date")

                transactions.append(
                    {
                        "file": filename,
                        "source_row": source_row,
                        "run_date": run_date,
                        "run_date_str": run_date_str,
                        "settlement_date": parse_optional_date(settlement_date_str),
                        "settlement_date_str": settlement_date_str,
                        "account": account,
                        "account_num": account_num,
                        "action": action,
                        "symbol": symbol,
                        "desc": description,
                        "tx_type": value(row, "Type"),
                        "qty": qty,
                        "price": price,
                        "comm_str": value(row, "Commission ($)"),
                        "fees_str": value(row, "Fees ($)"),
                        "interest_str": value(row, "Accrued Interest ($)"),
                        "amount": amount,
                        **classification,
                    }
                )

    transactions.sort(key=transaction_sort_key)
    return transactions, warnings


def _position_side(tx, positions):
    """Resolve opening/closing intent and the position side affected."""
    action_side = tx["action_side"]
    key = (tx["account_num"], tx["symbol"])

    if tx["is_opening"]:
        return "Opening", action_side
    if tx["is_closing"]:
        return "Closing", -action_side

    opposite_lots = positions.get((key, -action_side))
    if opposite_lots:
        return "Closing", -action_side
    return "Opening", action_side


def _validate_closing(tx, original_qty):
    matched = tx["_matched_qty"]
    unmatched = tx["_unmatched_qty"]
    if matched < ZERO or unmatched < ZERO:
        raise RuntimeError("FIFO reconciliation failed: negative matched quantity")
    if abs(original_qty - matched - unmatched) > QTY_TOLERANCE:
        raise RuntimeError(
            "FIFO reconciliation failed for "
            f"{tx['file']}:{tx['source_row']}: closed quantity does not balance"
        )


def _validate_open_lots(positions):
    for lots in positions.values():
        for lot in lots:
            if lot["qty"] < -QTY_TOLERANCE:
                raise RuntimeError("FIFO reconciliation failed: negative open-lot quantity")
            if abs(lot["initial_qty"] - lot["qty"] - lot["matched_qty"]) > QTY_TOLERANCE:
                raise RuntimeError("FIFO reconciliation failed: open lot does not balance")


def _validate_lot(lot):
    if lot["qty"] < -QTY_TOLERANCE:
        raise RuntimeError("FIFO reconciliation failed: negative open-lot quantity")
    if abs(lot["initial_qty"] - lot["qty"] - lot["matched_qty"]) > QTY_TOLERANCE:
        raise RuntimeError("FIFO reconciliation failed: open lot does not balance")


def match_transactions(transactions, cutoff_date):
    """Apply direction-aware FIFO matching and validate quantity conservation."""
    positions = {}
    results = []
    warnings = []

    for original in sorted(transactions, key=transaction_sort_key):
        tx = dict(original)
        tx.update(
            {
                "closed_qty_pre_cutoff": "",
                "closed_qty_post_cutoff": "",
                "closed_qty_pre_existing": "",
                "profit_pre_cutoff": "",
                "profit_post_cutoff": "",
                "profit_pre_existing": "",
                "trade_type": "N/A",
                "_matched_qty": ZERO,
                "_unmatched_qty": ZERO,
            }
        )

        if not tx["is_trade"]:
            results.append(tx)
            continue

        trade_type, position_side = _position_side(tx, positions)
        tx["trade_type"] = trade_type
        quantity = abs(tx["qty"])
        key = (tx["account_num"], tx["symbol"])
        position_key = (key, position_side)

        if quantity <= QTY_TOLERANCE:
            warnings.append(
                f"{tx['file']}:{tx['source_row']}: zero-quantity {trade_type.lower()} ignored"
            )
            if trade_type == "Closing":
                _validate_closing(tx, quantity)
            results.append(tx)
            continue

        if trade_type == "Opening":
            positions.setdefault(position_key, deque()).append(
                {
                    "run_date": tx["run_date"],
                    "qty": quantity,
                    "initial_qty": quantity,
                    "matched_qty": ZERO,
                    "amount": tx["amount"],
                }
            )
            results.append(tx)
            continue

        remaining = quantity
        lots = positions.get(position_key, deque())
        closing_unit_cash = tx["amount"] / quantity
        quantities = {"pre": ZERO, "post": ZERO}
        profits = {"pre": ZERO, "post": ZERO}

        while remaining > QTY_TOLERANCE and lots:
            lot = lots[0]
            matched = min(remaining, lot["qty"])
            opening_unit_cash = lot["amount"] / lot["initial_qty"]
            profit = matched * (closing_unit_cash + opening_unit_cash)
            period = "pre" if lot["run_date"] < cutoff_date else "post"
            quantities[period] += matched
            profits[period] += profit

            remaining -= matched
            lot["qty"] -= matched
            lot["matched_qty"] += matched
            tx["_matched_qty"] += matched
            _validate_lot(lot)
            if lot["qty"] <= QTY_TOLERANCE:
                lots.popleft()

        tx["_unmatched_qty"] = remaining
        if quantities["pre"] > QTY_TOLERANCE:
            tx["closed_qty_pre_cutoff"] = round_quantity(quantities["pre"])
            tx["profit_pre_cutoff"] = round_money(profits["pre"])
        if quantities["post"] > QTY_TOLERANCE:
            tx["closed_qty_post_cutoff"] = round_quantity(quantities["post"])
            tx["profit_post_cutoff"] = round_money(profits["post"])
        if remaining > QTY_TOLERANCE:
            tx["closed_qty_pre_existing"] = round_quantity(remaining)
            tx["profit_pre_existing"] = "Unknown"

        _validate_closing(tx, quantity)
        results.append(tx)

    _validate_open_lots(positions)
    return results, warnings


def write_analysis(output_file, transactions, cutoff_date):
    cutoff = cutoff_date.strftime("%Y-%m-%d")
    headers = [
        "Run Date", "Account", "Account Number", "Action", "Symbol", "Description",
        "Type", "Price ($)", "Quantity", "Commission ($)", "Fees ($)",
        "Accrued Interest ($)", "Amount ($)", "Settlement Date", "Is Trade",
        "Asset Type", "Trade Type", f"Closed Qty Pre-{cutoff}",
        f"Closed Qty Post-{cutoff}", "Closed Qty Pre-Existing",
        f"Profit Pre-{cutoff} ($)", f"Profit Post-{cutoff} ($)",
        "Profit Pre-Existing ($)",
    ]

    with open(output_file, "w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(headers)
        for tx in transactions:
            writer.writerow(
                [
                    tx["run_date_str"], tx["account"], tx["account_num"], tx["action"],
                    tx["symbol"], tx["desc"], tx["tx_type"],
                    tx["price"] if tx["price"] != ZERO else "", tx["qty"],
                    tx["comm_str"], tx["fees_str"], tx["interest_str"], tx["amount"],
                    tx["settlement_date_str"], tx["is_trade"], tx["asset_type"],
                    tx["trade_type"], tx["closed_qty_pre_cutoff"],
                    tx["closed_qty_post_cutoff"], tx["closed_qty_pre_existing"],
                    tx["profit_pre_cutoff"], tx["profit_post_cutoff"],
                    tx["profit_pre_existing"],
                ]
            )


def print_summary(transactions, cutoff_date):
    summary = {
        asset: {"pre_cutoff": ZERO, "post_cutoff": ZERO, "pre_exist_qty": ZERO}
        for asset in ("Put Option", "Call Option", "Stock")
    }
    for tx in transactions:
        if not tx["is_trade"] or tx["trade_type"] != "Closing":
            continue
        values = summary.get(tx["asset_type"])
        if values is None:
            continue
        if tx["profit_pre_cutoff"] != "":
            values["pre_cutoff"] += tx["profit_pre_cutoff"]
        if tx["profit_post_cutoff"] != "":
            values["post_cutoff"] += tx["profit_post_cutoff"]
        if tx["closed_qty_pre_existing"] != "":
            values["pre_exist_qty"] += tx["closed_qty_pre_existing"]

    cutoff = cutoff_date.strftime("%Y-%m-%d")
    print("\n" + "=" * 96)
    print(f"PROFIT/LOSS SUMMARY FOR TRANSACTIONS CLOSED ON/AFTER {cutoff}")
    print("=" * 96)
    print(
        f"{'Asset Type':<15} | {f'Opened Before {cutoff} ($)':<28} | "
        f"{f'Opened Since {cutoff} ($)':<28} | {'Unmatched Pre-Existing Qty':<26}"
    )
    print("-" * 108)
    total_pre = ZERO
    total_post = ZERO
    for asset, values in summary.items():
        print(
            f"{asset:<15} | {values['pre_cutoff']:>28,.2f} | "
            f"{values['post_cutoff']:>28,.2f} | "
            f"{values['pre_exist_qty']:>26,.3f}"
        )
        total_pre += values["pre_cutoff"]
        total_post += values["post_cutoff"]
    print("-" * 108)
    print(f"{'Total':<15} | {total_pre:>28,.2f} | {total_post:>28,.2f} |")
    print("=" * 96)


def process_transactions(input_dir, output_file, cutoff_date):
    """Orchestrate loading, matching, filtering, output, and reporting."""
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.", file=sys.stderr)
        return False

    transactions, load_warnings = load_transactions(input_dir)
    results, match_warnings = match_transactions(transactions, cutoff_date)
    output_transactions = [tx for tx in results if tx["run_date"] >= cutoff_date]
    write_analysis(output_file, output_transactions, cutoff_date)

    for warning in load_warnings + match_warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(f"Successfully generated analysis CSV at: {output_file}")
    print_summary(output_transactions, cutoff_date)
    return True


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Processes trading transaction CSVs using FIFO matching and attributes "
            "profit/loss across a date cutoff."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Example Usage:
  python3 process_transactions.py
  python3 process_transactions.py -i ./my_trades -d 01/01/2026 -o ./output.csv
""",
    )
    parser.add_argument(
        "-i", "--input-dir", default="./tr",
        help="Directory containing input CSV files (default: './tr')",
    )
    parser.add_argument(
        "-o", "--output-file", default="./transactions_analysis_post_615.csv",
        help="Output CSV path (default: './transactions_analysis_post_615.csv')",
    )
    parser.add_argument(
        "-d", "--cutoff-date", type=parse_date, default="06/15/2026",
        help="Attribution cutoff in MM/DD/YYYY format (default: '06/15/2026')",
    )
    return parser


if __name__ == "__main__":
    arguments = build_parser().parse_args()
    raise SystemExit(
        0
        if process_transactions(
            arguments.input_dir, arguments.output_file, arguments.cutoff_date
        )
        else 1
    )
