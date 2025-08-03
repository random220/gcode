#!/usr/bin/env python
import sys
import csv
import json

things = {}

with open('_closed.csv', 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Account'] != '':
            account = row['Account']
            if account not in things:
                things[account] = {}
        else:
            if row['Amount'] != '':
                amount = float(row['Amount'])
                date = int(row['Date'])
                if date not in things[account]:
                    things[account][date] = []
                things[account][date].append(amount)

#print(json.dumps(things, indent=2))

money = {}
for account in things:
    if account not in money:
        money[account] = {}
        money[account]['borrowed'] = 0
        money[account]['cash'] = 0

    for date in sorted(list(things[account].keys())):
        for amount in things[account][date]:
            newcash = money[account]['cash'] + amount
            if newcash < 0:
                money[account]['borrowed'] -= newcash
                money[account]['cash'] = 0
            else:
                money[account]['cash'] = newcash

print(json.dumps(money, indent=2))
