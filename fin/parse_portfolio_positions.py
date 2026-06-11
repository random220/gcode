#!/usr/bin/env python3
"""Parse a Fidelity Portfolio Positions CSV and sum Current Value per account."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

TAX_GROUPS: list[tuple[str, str]] = [
    ("anaya", "Anaya accounts"),
    ("brok", "Brokerage accounts"),
    ("hsa", "HSA accounts"),
    ("pretax", "401k / IRA / BrokerageLink accounts"),
    ("roth", "Roth accounts"),
    ("other", "Other accounts"),
]


def parse_currency(value: str | None) -> float | None:
    if value is None:
        return None

    text = str(value).strip()
    if not text or text == "--":
        return None

    text = text.replace("$", "").replace(",", "")
    if text.startswith("(") and text.endswith(")"):
        text = f"-{text[1:-1]}"

    try:
        return float(text)
    except ValueError:
        return None


def classify_account(account_name: str) -> str:
    lower = account_name.lower()

    if lower.startswith("anaya-") or "anaya" in lower:
        return "anaya"

    if lower.startswith("brok-") or "brokerage" in lower:
        return "brok"

    if lower.startswith("hsa-"):
        return "hsa"

    if (
        lower.startswith("401k-")
        or lower.startswith("ira-")
        or lower.startswith("blink-")
    ):
        return "pretax"

    if lower.startswith("rothi-") or lower.startswith("rothblink-"):
        return "roth"

    return "other"


def format_value(value: float) -> str:
    if value == 0:
        return "0"
    text = f"{value:.2f}"
    return text.rstrip("0").rstrip(".")


def parse_portfolio_positions(input_path: Path) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)

    with input_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            account_name = (row.get("Account Name") or "").strip()
            if not account_name:
                continue

            current_value = parse_currency(row.get("Current Value"))
            if current_value is None:
                continue

            totals[account_name] += current_value

    return dict(totals)


def group_account_totals(totals: dict[str, float]) -> dict[str, list[tuple[str, float]]]:
    grouped: dict[str, list[tuple[str, float]]] = {
        group_id: [] for group_id, _ in TAX_GROUPS
    }

    for account_name, value in totals.items():
        group_id = classify_account(account_name)
        grouped[group_id].append((account_name, value))

    for group_id in grouped:
        grouped[group_id].sort(key=lambda item: item[0].lower())

    return grouped


def write_flat_account_totals(totals: dict[str, float], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Account-Name", "Value"])
        for account_name, value in sorted(totals.items(), key=lambda item: (-item[1], item[0])):
            writer.writerow([account_name, format_value(value)])


def write_grouped_account_totals(
    grouped: dict[str, list[tuple[str, float]]], output_path: Path
) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Account-Name", "Value"])

        for group_id, _ in TAX_GROUPS:
            accounts = grouped[group_id]
            if not accounts:
                continue

            writer.writerow(["", ""])

            group_total = 0.0
            for account_name, value in accounts:
                writer.writerow([account_name, format_value(value)])
                group_total += value

            writer.writerow(["", ""])
            writer.writerow(["", format_value(group_total)])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sum portfolio position values by account name."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="Portfolio_Positions_Jun-11-2026.csv",
        help="Input Fidelity portfolio positions CSV",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="account_totals.csv",
        help="Output CSV path (default: account_totals.csv)",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Write one row per account without tax-group subtotals",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    totals = parse_portfolio_positions(input_path)

    if args.flat:
        write_flat_account_totals(totals, output_path)
        print(f"Wrote {len(totals)} accounts to {output_path}")
        for account_name, value in sorted(totals.items(), key=lambda item: (-item[1], item[0])):
            print(f"  {account_name}: ${value:,.2f}")
        return

    grouped = group_account_totals(totals)
    write_grouped_account_totals(grouped, output_path)

    print(f"Wrote grouped account totals to {output_path}")
    for group_id, label in TAX_GROUPS:
        accounts = grouped[group_id]
        if not accounts:
            continue

        group_total = sum(value for _, value in accounts)
        print(f"\n{label}: ${group_total:,.2f}")
        for account_name, value in accounts:
            print(f"  {account_name}: ${value:,.2f}")

    other_accounts = grouped["other"]
    if other_accounts:
        print(
            "\nNote: accounts in the 'other' group did not match a tax-bucket prefix. "
            "Rename them in the input CSV if they should be grouped."
        )


if __name__ == "__main__":
    main()