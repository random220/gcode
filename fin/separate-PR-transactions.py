#!/usr/bin/env python3
"""
Transaction Profit/Loss matching and Period Attribution Script
==============================================================

Intent:
-------
This script scans a directory containing broker transaction CSV files, parses all 
records chronologically, and runs a FIFO (First-In, First-Out) matching engine.
It matches opening transactions (buy to open / sell to open) with closing transactions
(sell to close / buy to close) to calculate realized profits/losses.

The core goal is to attribute realized profits/losses of transactions executed on or 
after a specific threshold cutoff date (default: 6/15/2026) based on whether the 
positions were originally opened BEFORE or ON/AFTER that threshold date.

Implementation & Design:
-------------------------
1. Schema Normalization: Ignores leading empty lines and handles inconsistent column
   ordering dynamically (e.g., swapped 'Quantity' and 'Price ($)' columns between 
   2025 and 2026 CSV templates). Works with UTF-8 BOM encoding.
2. Chronological Ordering: Combines and sorts all transaction logs from oldest to 
   newest to rebuild complete trade histories.
3. FIFO Matching Engine: Maintains queues of open lots mapped per unique Account Number 
   and Symbol. Handles both long (buy-to-open) and short (sell-to-open) options/stocks.
4. Profit/Loss Attribution:
   - Uses net 'Amount ($)' cash flows (inclusive of broker commissions and fees).
   - If a closing trade closes a position built across multiple opening dates, the 
     script splits the trade dynamically to distribute realized profits between the 
     pre-threshold and post-threshold periods.
   - Positions opened before the dataset's earliest record (1/23/2025) are flagged
     as 'Pre-Existing' with 'Unknown' profits.
5. Command Line Interface: Parametrized using argparse for directories, files, and dates.
"""

import os
import csv
import argparse
from datetime import datetime

def parse_date(date_str):
    """Parse MM/DD/YYYY date string into a datetime object."""
    try:
        return datetime.strptime(date_str.strip(), '%m/%d/%Y')
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_str}'. Must be MM/DD/YYYY.")

def process_transactions(input_dir, output_file, cutoff_date):
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return
        
    all_txs = []

    # 1. Parse all CSV files in the input directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.csv'):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
                # Find the header row (skip leading blank lines)
                header_idx = 0
                while header_idx < len(lines) and not lines[header_idx].strip():
                    header_idx += 1
                if header_idx >= len(lines):
                    continue
                
                reader = csv.reader(lines[header_idx:])
                try:
                    header = [h.strip() for h in next(reader)]
                except StopIteration:
                    continue
                
                col_map = {col: i for i, col in enumerate(header)}
                required = ['Run Date', 'Account Number', 'Action', 'Symbol', 'Quantity', 'Amount ($)']
                missing = [r for r in required if r not in col_map]
                if missing:
                    print(f"Warning: File {filename} is missing required columns: {missing}. Skipping.")
                    continue
                
                for row in reader:
                    if not row or len(row) < len(col_map):
                        continue
                    
                    run_date_str = row[col_map['Run Date']].strip()
                    account = row[col_map['Account']].strip() if 'Account' in col_map else ''
                    account_num = row[col_map['Account Number']].strip()
                    
                    # Restrict parsing to the two brokerage accounts: brok1 and brok2 (only these are relevant for taxes)
                    acc_lower = account.lower().replace('-', '').replace(' ', '')
                    is_brok1 = 'brok1' in acc_lower or account_num == 'X96600886'
                    is_brok2 = 'brok2' in acc_lower or account_num == 'Z34395861'
                    if not (is_brok1 or is_brok2):
                        continue
                    action = row[col_map['Action']].strip()
                    symbol = row[col_map['Symbol']].strip()
                    desc = row[col_map['Description']].strip() if 'Description' in col_map else ''
                    tx_type = row[col_map['Type']].strip() if 'Type' in col_map else ''
                    qty_str = row[col_map['Quantity']].strip()
                    price_str = row[col_map['Price ($)']].strip() if 'Price ($)' in col_map else ''
                    comm_str = row[col_map['Commission ($)']].strip() if 'Commission ($)' in col_map else ''
                    fees_str = row[col_map['Fees ($)']].strip() if 'Fees ($)' in col_map else ''
                    interest_str = row[col_map['Accrued Interest ($)']].strip() if 'Accrued Interest ($)' in col_map else ''
                    amount_str = row[col_map['Amount ($)']].strip()
                    settlement_date_str = row[col_map['Settlement Date']].strip() if 'Settlement Date' in col_map else ''
                    
                    if not run_date_str:
                        continue
                    
                    try:
                        run_date = datetime.strptime(run_date_str, '%m/%d/%Y')
                    except ValueError:
                        continue
                    
                    try:
                        qty = float(qty_str.replace(',', '')) if qty_str else 0.0
                    except ValueError:
                        qty = 0.0
                    
                    try:
                        amount = float(amount_str.replace(',', '').replace('$', '')) if amount_str else 0.0
                    except ValueError:
                        amount = 0.0
                    
                    try:
                        price = float(price_str.replace(',', '').replace('$', '')) if price_str else 0.0
                    except ValueError:
                        price = 0.0
                    
                    action_upper = action.upper()
                    is_trade = False
                    is_opening = False
                    is_closing = False
                    
                    is_option = symbol.startswith('-') or (symbol.startswith(' ') and '-' in symbol) or 'CALL (' in action_upper or 'PUT (' in action_upper
                    
                    asset_type = 'Other'
                    if 'BOUGHT' in action_upper or 'SOLD' in action_upper:
                        is_trade = True
                        if is_option:
                            if 'PUT' in action_upper or 'PUT' in symbol.upper():
                                asset_type = 'Put Option'
                            else:
                                asset_type = 'Call Option'
                        else:
                            asset_type = 'Stock'
                            
                        if 'OPENING' in action_upper:
                            is_opening = True
                        elif 'CLOSING' in action_upper:
                            is_closing = True

                    all_txs.append({
                        'file': filename,
                        'run_date': run_date,
                        'run_date_str': run_date_str,
                        'account': account,
                        'account_num': account_num,
                        'action': action,
                        'symbol': symbol,
                        'desc': desc,
                        'tx_type': tx_type,
                        'qty': qty,
                        'price': price,
                        'comm_str': comm_str,
                        'fees_str': fees_str,
                        'interest_str': interest_str,
                        'amount': amount,
                        'settlement_date_str': settlement_date_str,
                        'is_trade': is_trade,
                        'is_opening': is_opening,
                        'is_closing': is_closing,
                        'asset_type': asset_type,
                        'raw_row': row
                    })

    # 2. Sort transactions chronologically
    all_txs.sort(key=lambda x: (x['run_date'], x['file']))

    # 3. FIFO Matching Logic
    open_positions = {}
    results = []

    for tx in all_txs:
        tx['closed_qty_pre_cutoff'] = ''
        tx['closed_qty_post_cutoff'] = ''
        tx['closed_qty_pre_existing'] = ''
        tx['profit_pre_cutoff'] = ''
        tx['profit_post_cutoff'] = ''
        tx['profit_pre_existing'] = ''
        tx['trade_type'] = 'N/A'
        
        if not tx['is_trade']:
            results.append(tx)
            continue
        
        key = (tx['account_num'], tx['symbol'])
        qty = tx['qty']
        amount = tx['amount']
        
        is_opening = tx['is_opening']
        is_closing = tx['is_closing']
        
        if not is_opening and not is_closing:
            current_lots = open_positions.get(key, [])
            current_qty = sum(lot['qty'] for lot in current_lots)
            if current_qty == 0:
                is_opening = True
            elif (current_qty > 0 and qty > 0) or (current_qty < 0 and qty < 0):
                is_opening = True
            else:
                is_closing = True
                
        if is_opening:
            tx['trade_type'] = 'Opening'
            if key not in open_positions:
                open_positions[key] = []
            open_positions[key].append({
                'run_date': tx['run_date'],
                'run_date_str': tx['run_date_str'],
                'qty': abs(qty),
                'initial_qty': abs(qty),
                'amount': amount
            })
        elif is_closing:
            tx['trade_type'] = 'Closing'
            close_qty = abs(qty)
            current_lots = open_positions.get(key, [])
            
            closing_unit_cash = amount / close_qty
            
            c_qty_pre = 0.0
            c_qty_post = 0.0
            c_qty_pre_exist = 0.0
            prof_pre = 0.0
            prof_post = 0.0
            
            while close_qty > 1e-6 and current_lots:
                lot = current_lots[0]
                matched_qty = min(close_qty, lot['qty'])
                
                lot_unit_cash = lot['amount'] / lot['initial_qty']
                chunk_profit = matched_qty * (closing_unit_cash + lot_unit_cash)
                
                if lot['run_date'] < cutoff_date:
                    c_qty_pre += matched_qty
                    prof_pre += chunk_profit
                else:
                    c_qty_post += matched_qty
                    prof_post += chunk_profit
                    
                close_qty -= matched_qty
                lot['qty'] -= matched_qty
                if lot['qty'] <= 1e-6:
                    current_lots.pop(0)
                    
            if close_qty > 1e-6:
                c_qty_pre_exist += close_qty
            
            if c_qty_pre > 0:
                tx['closed_qty_pre_cutoff'] = round(c_qty_pre, 4)
                tx['profit_pre_cutoff'] = round(prof_pre, 2)
            if c_qty_post > 0:
                tx['closed_qty_post_cutoff'] = round(c_qty_post, 4)
                tx['profit_post_cutoff'] = round(prof_post, 2)
            if c_qty_pre_exist > 0:
                tx['closed_qty_pre_existing'] = round(c_qty_pre_exist, 4)
                tx['profit_pre_existing'] = 'Unknown'
                
        results.append(tx)

    # 4. Filter results for transactions done on or after cutoff_date
    output_txs = [tx for tx in results if tx['run_date'] >= cutoff_date]

    # 5. Write to CSV file
    cutoff_date_str = cutoff_date.strftime('%Y-%m-%d')
    headers = [
        'Run Date', 'Account', 'Account Number', 'Action', 'Symbol', 'Description', 'Type',
        'Price ($)', 'Quantity', 'Commission ($)', 'Fees ($)', 'Accrued Interest ($)', 'Amount ($)', 'Settlement Date',
        'Is Trade', 'Asset Type', 'Trade Type',
        f'Closed Qty Pre-{cutoff_date_str}', f'Closed Qty Post-{cutoff_date_str}', 'Closed Qty Pre-Existing',
        f'Profit Pre-{cutoff_date_str} ($)', f'Profit Post-{cutoff_date_str} ($)', 'Profit Pre-Existing ($)'
    ]

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for tx in output_txs:
            writer.writerow([
                tx['run_date_str'],
                tx['account'],
                tx['account_num'],
                tx['action'],
                tx['symbol'],
                tx['desc'],
                tx['tx_type'],
                tx['price'] if tx['price'] != 0.0 else '',
                tx['qty'],
                tx['comm_str'],
                tx['fees_str'],
                tx['interest_str'],
                tx['amount'],
                tx['settlement_date_str'],
                tx['is_trade'],
                tx['asset_type'],
                tx['trade_type'],
                tx['closed_qty_pre_cutoff'],
                tx['closed_qty_post_cutoff'],
                tx['closed_qty_pre_existing'],
                tx['profit_pre_cutoff'],
                tx['profit_post_cutoff'],
                tx['profit_pre_existing']
            ])

    print(f"Successfully generated analysis CSV at: {output_file}")

    # 6. Print Summary
    summary = {
        'Put Option': {'pre_cutoff': 0.0, 'post_cutoff': 0.0, 'pre_exist_qty': 0.0},
        'Call Option': {'pre_cutoff': 0.0, 'post_cutoff': 0.0, 'pre_exist_qty': 0.0},
        'Stock': {'pre_cutoff': 0.0, 'post_cutoff': 0.0, 'pre_exist_qty': 0.0}
    }

    for tx in output_txs:
        if tx['is_trade'] and tx['trade_type'] == 'Closing':
            at = tx['asset_type']
            if at in summary:
                if tx['profit_pre_cutoff']:
                    summary[at]['pre_cutoff'] += tx['profit_pre_cutoff']
                if tx['profit_post_cutoff']:
                    summary[at]['post_cutoff'] += tx['profit_post_cutoff']
                if tx['closed_qty_pre_existing']:
                    summary[at]['pre_exist_qty'] += tx['closed_qty_pre_existing']

    print("\n" + "="*96)
    print(f"PROFIT/LOSS SUMMARY FOR TRANSACTIONS CLOSED ON/AFTER {cutoff_date_str}")
    print("="*96)
    print(f"{'Asset Type':<15} | {f'Opened Before {cutoff_date_str} ($)':<28} | {f'Opened Since {cutoff_date_str} ($)':<28} | {'Unmatched Pre-Existing Qty':<26}")
    print("-"*108)
    tot_pre = 0.0
    tot_post = 0.0
    for at, vals in summary.items():
        print(f"{at:<15} | {vals['pre_cutoff']:>28,.2f} | {vals['post_cutoff']:>28,.2f} | {vals['pre_exist_qty']:>26,.3f}")
        tot_pre += vals['pre_cutoff']
        tot_post += vals['post_cutoff']
    print("-"*108)
    print(f"{'Total':<15} | {tot_pre:>28,.2f} | {tot_post:>28,.2f} |")
    print("="*96)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Processes trading transactions CSVs using FIFO matching and attributes profit/loss across a date cutoff.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example Usage:
--------------
  # Use defaults (scans ./tr, outputs to ./transactions_analysis_post_615.csv, threshold 6/15/2026)
  python3 process_transactions.py

  # Custom directory and cutoff date
  python3 process_transactions.py -i ./my_trades -d 01/01/2026 -o ./output_2026.csv
"""
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        default='./tr',
        help="Directory containing the input CSV files (default: './tr')"
    )
    
    parser.add_argument(
        '-o', '--output-file',
        default='./transactions_analysis_post_615.csv',
        help="Path where the output decorated CSV should be written (default: './transactions_analysis_post_615.csv')"
    )
    
    parser.add_argument(
        '-d', '--cutoff-date',
        type=parse_date,
        default='06/15/2026',
        help="Attribution threshold cutoff date in MM/DD/YYYY format (default: '06/15/2026')"
    )

    args = parser.parse_args()
    process_transactions(args.input_dir, args.output_file, args.cutoff_date)
