import csv
from datetime import datetime

# Load data
with open('a.csv', newline='') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Convert dates
for row in data:
    row['Run Date'] = datetime.strptime(row['Run Date'], '%m/%d/%Y')

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
