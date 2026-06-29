import csv
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from decimal import Decimal
from io import StringIO

from process_transactions import (
    LONG,
    SHORT,
    _position_side,
    classify_asset,
    classify_trade,
    load_transactions,
    match_transactions,
    parse_decimal,
    print_summary,
    process_transactions,
    transaction_sort_key,
    write_analysis,
)


CUTOFF = datetime(2026, 6, 15)

BROKER_HEADER = [
    "Run Date",
    "Account",
    "Account Number",
    "Action",
    "Symbol",
    "Description",
    "Type",
    "Price ($)",
    "Quantity",
    "Commission ($)",
    "Fees ($)",
    "Accrued Interest ($)",
    "Amount ($)",
    "Settlement Date",
]


def transaction(
    action,
    qty,
    amount,
    *,
    date=datetime(2026, 6, 20),
    symbol="ABC",
    filename="input.csv",
    row=1,
):
    classification = classify_trade(action, symbol, "")
    return {
        "file": filename,
        "source_row": row,
        "run_date": date,
        "run_date_str": date.strftime("%m/%d/%Y"),
        "settlement_date": None,
        "settlement_date_str": "",
        "account": "Brok1",
        "account_num": "X96600886",
        "action": action,
        "symbol": symbol,
        "desc": "",
        "tx_type": "Cash",
        "qty": Decimal(qty),
        "price": Decimal("0"),
        "comm_str": "",
        "fees_str": "",
        "interest_str": "",
        "amount": Decimal(amount),
        **classification,
    }


def write_broker_csv(directory, filename, rows):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(BROKER_HEADER)
        for row in rows:
            writer.writerow(row)
    return path


def read_csv_rows(path):
    with open(path, encoding="utf-8", newline="") as source:
        return list(csv.reader(source))


class DecimalTests(unittest.TestCase):
    def test_decimal_arithmetic_is_exact(self):
        self.assertEqual(parse_decimal("0.1") + parse_decimal("0.2"), Decimal("0.3"))
        self.assertEqual(parse_decimal("$1,234.56"), Decimal("1234.56"))


class ClassificationTests(unittest.TestCase):
    def test_occ_symbols_classify_call_and_put(self):
        self.assertEqual(classify_asset(" -AAPL260918C220"), "Call Option")
        self.assertEqual(classify_asset("-SPY260918P500.5"), "Put Option")

    def test_description_fallback_and_stock(self):
        self.assertEqual(classify_asset("", "PUT (SPY) SEP 18 26"), "Put Option")
        self.assertEqual(classify_asset("AAPL", "APPLE INC"), "Stock")

    def test_action_side_is_independent_of_quantity_sign(self):
        self.assertEqual(
            classify_trade("YOU BOUGHT OPENING TRANSACTION", "ABC")["action_side"],
            LONG,
        )
        self.assertEqual(
            classify_trade("YOU SOLD OPENING TRANSACTION", "ABC")["action_side"],
            SHORT,
        )


class OrderingTests(unittest.TestCase):
    def test_same_day_order_has_explicit_stable_tiebreakers(self):
        later_file = transaction("YOU BOUGHT", "1", "-10", filename="b.csv", row=1)
        later_row = transaction("YOU BOUGHT", "1", "-10", filename="a.csv", row=2)
        earlier_row = transaction("YOU BOUGHT", "1", "-10", filename="a.csv", row=1)
        ordered = sorted([later_file, later_row, earlier_row], key=transaction_sort_key)
        self.assertEqual(
            [(tx["file"], tx["source_row"]) for tx in ordered],
            [("a.csv", 1), ("a.csv", 2), ("b.csv", 1)],
        )


class PositionSideTests(unittest.TestCase):
    def test_explicit_opening_and_closing_tags(self):
        opening_tx = transaction("YOU BOUGHT OPENING TRANSACTION", "1", "-10")
        closing_tx = transaction("YOU SOLD CLOSING TRANSACTION", "-1", "12")
        self.assertEqual(_position_side(opening_tx, {}), ("Opening", LONG))
        self.assertEqual(_position_side(closing_tx, {}), ("Closing", LONG))

    def test_inferred_opening_when_no_opposite_lots(self):
        buy_tx = transaction("YOU BOUGHT", "5", "-50")
        self.assertEqual(_position_side(buy_tx, {}), ("Opening", LONG))

    def test_inferred_closing_when_opposite_lots_exist(self):
        key = ("X96600886", "ABC")
        positions = {
            (key, LONG): [
                {
                    "run_date": datetime(2026, 6, 10),
                    "qty": Decimal("5"),
                    "initial_qty": Decimal("5"),
                    "matched_qty": Decimal("0"),
                    "amount": Decimal("-50"),
                }
            ]
        }
        sell_tx = transaction("YOU SOLD", "-3", "36")
        self.assertEqual(_position_side(sell_tx, positions), ("Closing", LONG))

    def test_inferred_closing_on_short_cover(self):
        key = ("X96600886", "ABC")
        positions = {
            (key, SHORT): [
                {
                    "run_date": datetime(2026, 6, 10),
                    "qty": Decimal("5"),
                    "initial_qty": Decimal("5"),
                    "matched_qty": Decimal("0"),
                    "amount": Decimal("100"),
                }
            ]
        }
        buy_tx = transaction("YOU BOUGHT", "2", "-30")
        self.assertEqual(_position_side(buy_tx, positions), ("Closing", SHORT))

    def test_inferred_close_via_matching(self):
        opening = transaction("YOU BOUGHT", "5", "-50", row=1)
        closing = transaction("YOU SOLD", "-3", "36", row=2)
        results, warnings = match_transactions([opening, closing], CUTOFF)
        self.assertEqual(warnings, [])
        self.assertEqual(results[0]["trade_type"], "Opening")
        self.assertEqual(results[1]["trade_type"], "Closing")
        self.assertEqual(results[1]["profit_post_cutoff"], Decimal("6.00"))


class MatchingTests(unittest.TestCase):
    def test_long_fifo_profit(self):
        opening = transaction("YOU BOUGHT OPENING TRANSACTION", "10", "-100", row=1)
        closing = transaction("YOU SOLD CLOSING TRANSACTION", "-4", "60", row=2)
        results, warnings = match_transactions([closing, opening], CUTOFF)
        close_result = results[1]
        self.assertEqual(warnings, [])
        self.assertEqual(close_result["closed_qty_post_cutoff"], Decimal("4.0000"))
        self.assertEqual(close_result["profit_post_cutoff"], Decimal("20.00"))
        self.assertEqual(close_result["_matched_qty"], Decimal("4"))
        self.assertEqual(close_result["_unmatched_qty"], Decimal("0"))

    def test_short_fifo_profit(self):
        opening = transaction("YOU SOLD OPENING TRANSACTION", "-5", "100", row=1)
        closing = transaction("YOU BOUGHT CLOSING TRANSACTION", "2", "-30", row=2)
        results, _ = match_transactions([opening, closing], CUTOFF)
        close_result = results[1]
        self.assertEqual(close_result["profit_post_cutoff"], Decimal("10.00"))
        self.assertEqual(close_result["_matched_qty"], Decimal("2"))

    def test_zero_quantity_close_does_not_divide(self):
        closing = transaction("YOU SOLD CLOSING TRANSACTION", "0", "0", row=1)
        results, warnings = match_transactions([closing], CUTOFF)
        self.assertEqual(results[0]["_matched_qty"], Decimal("0"))
        self.assertEqual(results[0]["_unmatched_qty"], Decimal("0"))
        self.assertEqual(len(warnings), 1)

    def test_unmatched_close_reconciles_to_pre_existing(self):
        opening = transaction("YOU BOUGHT OPENING TRANSACTION", "2", "-20", row=1)
        closing = transaction("YOU SOLD CLOSING TRANSACTION", "-5", "75", row=2)
        results, _ = match_transactions([opening, closing], CUTOFF)
        close_result = results[1]
        self.assertEqual(close_result["_matched_qty"], Decimal("2"))
        self.assertEqual(close_result["_unmatched_qty"], Decimal("3"))
        self.assertEqual(
            close_result["_matched_qty"] + close_result["_unmatched_qty"],
            abs(closing["qty"]),
        )
        self.assertEqual(close_result["closed_qty_pre_existing"], Decimal("3.0000"))

    def test_fifo_close_splits_profit_across_cutoff(self):
        before = transaction(
            "YOU BOUGHT OPENING TRANSACTION",
            "2",
            "-20",
            date=datetime(2026, 6, 14),
            row=1,
        )
        after = transaction(
            "YOU BOUGHT OPENING TRANSACTION",
            "3",
            "-60",
            date=datetime(2026, 6, 15),
            row=2,
        )
        closing = transaction(
            "YOU SOLD CLOSING TRANSACTION",
            "-4",
            "100",
            date=datetime(2026, 6, 20),
            row=3,
        )
        results, _ = match_transactions([closing, after, before], CUTOFF)
        close_result = results[2]
        self.assertEqual(close_result["closed_qty_pre_cutoff"], Decimal("2.0000"))
        self.assertEqual(close_result["closed_qty_post_cutoff"], Decimal("2.0000"))
        self.assertEqual(close_result["profit_pre_cutoff"], Decimal("30.00"))
        self.assertEqual(close_result["profit_post_cutoff"], Decimal("10.00"))

    def test_opening_on_cutoff_date_is_post_cutoff(self):
        on_cutoff = transaction(
            "YOU BOUGHT OPENING TRANSACTION",
            "2",
            "-20",
            date=datetime(2026, 6, 15),
            row=1,
        )
        closing = transaction(
            "YOU SOLD CLOSING TRANSACTION",
            "-2",
            "30",
            date=datetime(2026, 6, 20),
            row=2,
        )
        results, _ = match_transactions([on_cutoff, closing], CUTOFF)
        close_result = results[1]
        self.assertEqual(close_result["closed_qty_pre_cutoff"], "")
        self.assertEqual(close_result["closed_qty_post_cutoff"], Decimal("2.0000"))
        self.assertEqual(close_result["profit_post_cutoff"], Decimal("10.00"))


class LoadTransactionsTests(unittest.TestCase):
    def test_loads_relevant_account_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            write_broker_csv(
                directory,
                "trades.csv",
                [
                    [
                        "06/20/2026",
                        "Brok1",
                        "X96600886",
                        "YOU BOUGHT OPENING TRANSACTION",
                        "ABC",
                        "",
                        "Cash",
                        "",
                        "10",
                        "",
                        "",
                        "",
                        "-100",
                        "",
                    ],
                    [
                        "06/20/2026",
                        "Other",
                        "99999999",
                        "YOU BOUGHT OPENING TRANSACTION",
                        "XYZ",
                        "",
                        "Cash",
                        "",
                        "1",
                        "",
                        "",
                        "",
                        "-10",
                        "",
                    ],
                ],
            )
            transactions, warnings = load_transactions(directory)
            self.assertEqual(warnings, [])
            self.assertEqual(len(transactions), 1)
            self.assertEqual(transactions[0]["symbol"], "ABC")
            self.assertEqual(transactions[0]["qty"], Decimal("10"))

    def test_missing_columns_skips_file_with_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "bad.csv")
            with open(path, "w", encoding="utf-8", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(["Run Date", "Action"])
                writer.writerow(["06/20/2026", "YOU BOUGHT"])
            transactions, warnings = load_transactions(directory)
            self.assertEqual(transactions, [])
            self.assertEqual(len(warnings), 1)
            self.assertIn("missing columns", warnings[0])

    def test_invalid_run_date_skips_row_with_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            write_broker_csv(
                directory,
                "trades.csv",
                [
                    [
                        "not-a-date",
                        "Brok1",
                        "X96600886",
                        "YOU BOUGHT",
                        "ABC",
                        "",
                        "Cash",
                        "",
                        "1",
                        "",
                        "",
                        "",
                        "-10",
                        "",
                    ]
                ],
            )
            transactions, warnings = load_transactions(directory)
            self.assertEqual(transactions, [])
            self.assertEqual(len(warnings), 1)
            self.assertIn("invalid Run Date", warnings[0])

    def test_empty_header_file_is_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "empty.csv")
            with open(path, "w", encoding="utf-8", newline="") as target:
                target.write("\n\n")
            transactions, warnings = load_transactions(directory)
            self.assertEqual(transactions, [])
            self.assertEqual(warnings, [])

    def test_account_number_filter_without_broker_name(self):
        with tempfile.TemporaryDirectory() as directory:
            write_broker_csv(
                directory,
                "trades.csv",
                [
                    [
                        "06/20/2026",
                        "",
                        "Z34395861",
                        "YOU BOUGHT",
                        "ABC",
                        "",
                        "Cash",
                        "",
                        "1",
                        "",
                        "",
                        "",
                        "-10",
                        "",
                    ]
                ],
            )
            transactions, warnings = load_transactions(directory)
            self.assertEqual(warnings, [])
            self.assertEqual(len(transactions), 1)
            self.assertEqual(transactions[0]["account_num"], "Z34395861")


class WriteAnalysisTests(unittest.TestCase):
    def test_output_headers_and_row_shape(self):
        closing = transaction("YOU SOLD CLOSING TRANSACTION", "-2", "30", row=2)
        opening = transaction("YOU BOUGHT OPENING TRANSACTION", "2", "-20", row=1)
        results, _ = match_transactions([opening, closing], CUTOFF)
        close_result = results[1]

        with tempfile.TemporaryDirectory() as directory:
            output_path = os.path.join(directory, "analysis.csv")
            write_analysis(output_path, [close_result], CUTOFF)
            rows = read_csv_rows(output_path)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "Run Date")
        self.assertIn("Closed Qty Pre-2026-06-15", rows[0])
        self.assertIn("Profit Post-2026-06-15 ($)", rows[0])
        self.assertEqual(rows[1][3], "YOU SOLD CLOSING TRANSACTION")
        self.assertEqual(rows[1][16], "Closing")
        self.assertEqual(rows[1][21], "10.00")


class PrintSummaryTests(unittest.TestCase):
    def test_summary_includes_asset_totals(self):
        opening = transaction("YOU BOUGHT OPENING TRANSACTION", "2", "-20", row=1)
        closing = transaction("YOU SOLD CLOSING TRANSACTION", "-2", "30", row=2)
        results, _ = match_transactions([opening, closing], CUTOFF)
        close_result = results[1]

        buffer = StringIO()
        with redirect_stdout(buffer):
            print_summary([close_result], CUTOFF)
        output = buffer.getvalue()

        self.assertIn("PROFIT/LOSS SUMMARY FOR TRANSACTIONS CLOSED ON/AFTER 2026-06-15", output)
        self.assertIn("Stock", output)
        self.assertIn("10.00", output)
        self.assertIn("Total", output)


class ProcessTransactionsTests(unittest.TestCase):
    def test_end_to_end_generates_filtered_output(self):
        with tempfile.TemporaryDirectory() as directory:
            write_broker_csv(
                directory,
                "trades.csv",
                [
                    [
                        "06/10/2026",
                        "Brok1",
                        "X96600886",
                        "YOU BOUGHT OPENING TRANSACTION",
                        "ABC",
                        "",
                        "Cash",
                        "",
                        "2",
                        "",
                        "",
                        "",
                        "-20",
                        "",
                    ],
                    [
                        "06/20/2026",
                        "Brok1",
                        "X96600886",
                        "YOU SOLD CLOSING TRANSACTION",
                        "ABC",
                        "",
                        "Cash",
                        "",
                        "-2",
                        "",
                        "",
                        "",
                        "30",
                        "",
                    ],
                ],
            )
            output_path = os.path.join(directory, "analysis.csv")
            stderr = StringIO()
            stdout = StringIO()
            with redirect_stderr(stderr), redirect_stdout(stdout):
                success = process_transactions(directory, output_path, CUTOFF)

            self.assertTrue(success)
            rows = read_csv_rows(output_path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1][0], "06/20/2026")
            self.assertEqual(rows[1][20], "10.00")
            self.assertIn("Successfully generated analysis CSV", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")

    def test_missing_input_directory_returns_false(self):
        stderr = StringIO()
        with redirect_stderr(stderr):
            success = process_transactions("/nonexistent/path", "out.csv", CUTOFF)
        self.assertFalse(success)
        self.assertIn("not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()