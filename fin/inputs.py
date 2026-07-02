#!/usr/bin/env python3
"""Filter Fidelity transaction exports to trade (BOUGHT/SOLD) rows only.

Usage:
    python inputs.py file1.csv [file2.csv ...]

Writes combined filtered rows to input.csv using the header from the first file.
"""

import csv
import sys
from pathlib import Path
from typing import Any


HEADER_KEY = "Run Date"


def read_trades(path: str | Path) -> tuple[list[str], list[dict[str, str]]]:
    """Return (fieldnames, list_of_trade_dicts) from a Fidelity CSV export.

    Robustly locates the header row (handles variable leading blank/BOM rows),
    strips UTF-8 BOM via encoding, and returns only rows whose Action contains
    BOUGHT or SOLD.
    """
    path = Path(path)
    with path.open("rt", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    # Locate header row
    header: list[str] | None = None
    data_start = 0
    for i, row in enumerate(rows):
        if row and row[0] == HEADER_KEY:
            header = row
            data_start = i + 1
            break

    if not header:
        return [], []

    n = len(header)
    trades: list[dict[str, str]] = []
    for row in rows[data_start:]:
        if len(row) != n:
            continue
        # Action is column index 3
        action = row[3]
        if "BOUGHT" in action or "SOLD" in action:
            trades.append(dict(zip(header, row)))

    return header, trades


def main(argv: list[str] = sys.argv) -> int:
    if len(argv) < 2:
        print("Usage: python inputs.py <csv> [csv ...]", file=sys.stderr)
        return 2

    all_trades: list[dict[str, str]] = []
    fieldnames: list[str] | None = None

    for csv_path in argv[1:]:
        hdr, trades = read_trades(csv_path)
        if hdr:
            if fieldnames is None:
                fieldnames = hdr
            all_trades.extend(trades)
            print(f"{csv_path}: {len(trades)} trades", file=sys.stderr)
        else:
            print(f"{csv_path}: no header found, skipped", file=sys.stderr)

    if not fieldnames:
        print("Error: no valid header found in any input file.", file=sys.stderr)
        return 1

    out_path = Path("input.csv")
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_trades)

    print(f"Wrote {len(all_trades)} total trades to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
