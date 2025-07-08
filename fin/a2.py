import csv
from datetime import datetime
import json

# Load data
with open('a.csv', newline='') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Convert dates
for row in data:
    row['Run Date'] = datetime.strptime(row['Run Date'], "%m/%d/%Y").strftime("%Y%m%d")

# print(json.dumps(data, indent=2))
# [
#   {
#     "Run Date": "20250331",
#     "Account": "VISA BrokerageLink",
#     "Account Number": "652344998",
#     "Action": "YOU BOUGHT OPENING TRANSACTION CALL (NVDA) NVIDIA CORPORATION OCT 17 25 $55 (100 SHS) (Cash)",
#     "Symbol": "-NVDA251017C55",
#     "Description": "CALL (NVDA) NVIDIA CORPORATION OCT 17 25 $55 (100 SHS)",
#     "Type": "Cash",
#     "Quantity": "1",
#     "Price ($)": "51.95",
#     "Commission ($)": "0.65",
#     "Fees ($)": "0.03",
#     "Accrued Interest ($)": "",
#     "Amount ($)": "-5195.68",
#     "Settlement Date": "04/01/2025"
#   },
#   {
#     "Run Date": "20250331",
#     "Account": "VISA BrokerageLink",
#     "Account Number": "652344998",
#     "Action": "YOU BOUGHT NVIDIA CORPORATION COM (NVDA) (Cash)",
#     "Symbol": "NVDA",
#     "Description": "NVIDIA CORPORATION COM",
#     "Type": "Cash",
#     "Quantity": "286",
#     "Price ($)": "104.82",
#     "Commission ($)": "",
#     "Fees ($)": "",
#     "Accrued Interest ($)": "",
#     "Amount ($)": "-29978.49",
#     "Settlement Date": "04/01/2025"
#   },
#   {
#     "Run Date": "20250331",
#     "Account": "VISA BrokerageLink",
#     "Account Number": "652344998",
#     "Action": "YOU BOUGHT NVIDIA CORPORATION COM (NVDA) (Cash)",
#     "Symbol": "NVDA",
#     "Description": "NVIDIA CORPORATION COM",
#     "Type": "Cash",
#     "Quantity": "0.205",
#     "Price ($)": "104.82",
#     "Commission ($)": "",
#     "Fees ($)": "",
#     "Accrued Interest ($)": "",
#     "Amount ($)": "-21.49",
#     "Settlement Date": "04/01/2025"
#   },
# ]

things = {}
for row in data:
    if row['Account Number'] not in things:
        things[row['Account Number']] = {}
    if row['Symbol'] not in things[row['Account Number']]:
        things[row['Account Number']][row['Symbol']] = {}
    if row['Run Date'] not in things[row['Account Number']][row['Symbol']]:
        things[row['Account Number']][row['Symbol']][row['Run Date']] = []
    things[row['Account Number']][row['Symbol']][row['Run Date']].append(row)

# print(json.dumps(things, indent=2))
# {
#   "652344998": {
#     "-NVDA251017C55": {
#       "20250331": [
#         {
#           "Run Date": "20250331",
#           "Account": "VISA BrokerageLink",
#           "Account Number": "652344998",
#           "Action": "YOU BOUGHT OPENING TRANSACTION CALL (NVDA) NVIDIA CORPORATION OCT 17 25 $55 (100 SHS) (Cash)",
#           "Symbol": "-NVDA251017C55",
#           "Description": "CALL (NVDA) NVIDIA CORPORATION OCT 17 25 $55 (100 SHS)",
#           "Type": "Cash",
#           "Quantity": "1",
#           "Price ($)": "51.95",
#           "Commission ($)": "0.65",
#           "Fees ($)": "0.03",
#           "Accrued Interest ($)": "",
#           "Amount ($)": "-5195.68",
#           "Settlement Date": "04/01/2025"
#         }
#       ],
#       "20250414": [
#         {
#           "Run Date": "20250414",
#           "Account": "VISA BrokerageLink",
#           "Account Number": "652344998",
#           "Action": "YOU SOLD CLOSING TRANSACTION CALL (NVDA) NVIDIA CORPORATION OCT 17 25 $55 (100 SHS) (Cash)",
#           "Symbol": "-NVDA251017C55",
#           "Description": "CALL (NVDA) NVIDIA CORPORATION OCT 17 25 $55 (100 SHS)",
#           "Type": "Cash",
#           "Quantity": "-6",
#           "Price ($)": "58",
#           "Commission ($)": "3.9",
#           "Fees ($)": "1.14",
#           "Accrued Interest ($)": "",
#           "Amount ($)": "34794.96",
#           "Settlement Date": "04/15/2025"
#         }
#       ],
#     },
#   },
# }

def linify(r):
    quantity = r['Quantity']
    price = r['Price ($)']
    comm = r['Commission ($)']
    fee = r['Fees ($)']
    amount = r['Amount ($)']
    return f'{quantity},{price},{comm},{fee},{amount}'

for account in things:
    for ticker in things[account]:
        print('----')
        count = 0
        rundates = sorted(things[account][ticker])
        for rundate in rundates:
            for row in things[account][ticker][rundate]:
                line = linify(row)
                print(f'{account},{ticker},{rundate},{line}')
                count += float(row['Quantity'])
                if count == 0:
                    print('xxxx')

'''
for ticker in things:
    rundates = sorted(list(things[ticker].keys()))
    for rundate in rundates:
        for r in things[ticker][rundate]:
            line = linify(r)
            print(f'{ticker},{rundate},{line}')

'''


'''
# Group by account and symbol
grouped_data = {}
for row in data:
    account = row['Account Number']
    symbol = row['Symbol']
    grouped_data.setdefault(account, {}).setdefault(symbol, []).append(row)

# Sort transactions
for account_data in grouped_data.values():
    for txns in account_data.values():
        txns.sort(key=lambda txn: txn['Run Date'])

# Convert dates back to strings
for account_data in grouped_data.values():
    for txns in account_data.values():
        for txn in txns:
            txn['Run Date'] = txn['Run Date'].strftime('%m/%d/%Y')

# Build clusters
clusters = []

for account, symbols in grouped_data.items():
    for symbol, txns in symbols.items():
        position = []
        sell_bucket = []
        buy_qty = 0
        sell_qty = 0

        for txn in txns:
            action = txn['Action']
            qty = float(txn['Quantity'])
            amt = float(txn['Amount ($)'])

            if 'BOUGHT' in action:
                position.append(txn)
                buy_qty += qty

            elif 'SOLD' in action:
                sell_bucket.append(txn)
                sell_qty += abs(qty)

                if sell_qty >= buy_qty and position:
                    invested = sum(float(p['Amount ($)']) for p in position)
                    proceeds = sum(float(s['Amount ($)']) for s in sell_bucket)
                    commission = sum(float(t['Commission ($)'] or 0) for t in position + sell_bucket)
                    fees = sum(float(t['Fees ($)'] or 0) for t in position + sell_bucket)
                    cost_total = commission + fees

                    raw_profit = proceeds + invested
                    profit = raw_profit - cost_total
                    return_pct = (profit / abs(invested)) * 100 if invested else 0.0

                    clusters.append({
                        'account': account,
                        'symbol': symbol,
                        'buys': position[:],
                        'sells': sell_bucket[:],
                        'summary': {
                            'return_pct': return_pct,
                            'invested': abs(invested),
                            'profit': profit,
                            'fees_and_comm': cost_total
                        },
                        'close_date': sell_bucket[-1]['Run Date']
                    })

                    # Reset for next cluster
                    position = []
                    sell_bucket = []
                    buy_qty = 0
                    sell_qty = 0

# Sort clusters by close date
clusters.sort(key=lambda c: datetime.strptime(c['close_date'], '%m/%d/%Y'))

# Write to CSV
with open('trade_clusters.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'Account', 'Symbol', 'Action', 'Date', 'Quantity',
        'Price', 'Amount', 'Return %', 'Invested', 'Profit', 'Fees + Commission'
    ])

    for c in clusters:
        writer.writerow([c['account'], c['symbol']])

        for b in c['buys']:
            writer.writerow([
                '', '', 'buy',
                b['Run Date'],
                b['Quantity'],
                f"@ ${b['Price ($)']}",
                f"${float(b['Amount ($)']):,.2f}"
            ])

        for s in c['sells']:
            writer.writerow([
                '', '', 'sell',
                s['Run Date'],
                s['Quantity'],
                f"@ ${s['Price ($)']}",
                f"${float(s['Amount ($)']):,.2f}"
            ])

        writer.writerow([
            '', '', '', '', '', '', '',
            f"{c['summary']['return_pct']:.2f}%",
            f"${c['summary']['invested']:,.2f}",
            f"${c['summary']['profit']:,.2f}",
            f"${c['summary']['fees_and_comm']:,.2f}"
        ])
        writer.writerow([])
'''
