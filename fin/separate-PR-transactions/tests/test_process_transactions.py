import unittest
from datetime import datetime
from decimal import Decimal

from process_transactions import (
    LONG,
    SHORT,
    classify_asset,
    classify_trade,
    match_transactions,
    parse_decimal,
    transaction_sort_key,
)


CUTOFF = datetime(2026, 6, 15)


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


if __name__ == "__main__":
    unittest.main()
