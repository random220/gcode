#!/usr/bin/env python

import csv
from datetime import datetime
import json

def main():
    data = read_data()
    data = bucketize_to_account_and_ticker(data)
    closed_clusters, open_clusters  = separate_closed_clusters(data)
    print_clusters(closed_clusters, '_closed.csv')
    print_clusters(open_clusters, '_open.csv')

def print_clusters(cl, fname):
    with open(fname, 'wt') as f:
        f.write(f'Account,Ticker,Date,Quantity,Price,Commission,Fees,Amount,Profit,Profit%,Investment\n')
        for account in cl:
            rundates = sorted(list(cl[account].keys()))
            for rundate in rundates:
                for ticker in cl[account][rundate]:
                    f.write(f'{account},{ticker},,,,,,\n')
                    for cluster in cl[account][rundate][ticker]:
                        print_cluster(f, cluster)

def print_cluster(f, cluster):
    buy_amount = 0
    sell_amount = 0
    Q = 0
    for row in cluster:
        rundate = row['Run Date']
        ticker = row['Symbol']
        quant = 0 if row['Quantity'] == '' else float(row['Quantity'])
        Q += quant
        price = 0 if row['Price ($)'] == '' else float(row['Price ($)'])
        commission = 0 if row['Commission ($)'] == '' else float(row['Commission ($)'])
        fees = 0 if row['Fees ($)'] == '' else float(row['Fees ($)'])
        amount = 0 if row['Amount ($)'] == '' else float(row['Amount ($)'])
        f.write(f',,{rundate},{quant},{price},{commission},{fees},{amount}\n')
        if amount < 0:
            buy_amount += amount
        else:
            sell_amount += amount
    if Q == 0:
        buy_amount = 0 - buy_amount
        profit = sell_amount - buy_amount
        profit_percentage = profit * 100 / buy_amount
        f.write(f',,,,,,,,{profit:.2f},{profit_percentage:.2f} %,{buy_amount:.2f}\n')
    f.write(f',,,,,,,,,,\n')

def separate_closed_clusters(data):
    clusters_closed = {}
    clusters_open = {}
    for account in data:
        for ticker in data[account]:
            cluster = []
            n = 0
            rundates = sorted(list(data[account][ticker].keys()))
            for rundate in rundates:
                for row in data[account][ticker][rundate]:
                    cluster.append(row)
                    n += float(row['Quantity'])
                    if n == 0:
                        cluster_add(clusters_closed, cluster, account, ticker, rundate)
                        cluster = []
            if len(cluster) != 0:
                cluster_add(clusters_open, cluster, account, ticker, rundate)
    return clusters_closed, clusters_open

def cluster_add(dest_dict, cluster, account, ticker, rundate):
    if account not in dest_dict:
        dest_dict[account] = {}
    if rundate not in dest_dict[account]:
        dest_dict[account][rundate] = {}
    if ticker not in  dest_dict[account][rundate]:
         dest_dict[account][rundate][ticker] = []
    dest_dict[account][rundate][ticker].append(cluster)

def bucketize_to_account_and_ticker(data):
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

    return things

def read_data():
    # Load data
    with open('input.csv', newline='') as file:
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
    return data

main()
