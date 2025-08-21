#!/usr/bin/env python3

import json
import csv
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple
import logging
from statistics import median, mean

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_data(input_file: str = 'input.csv') -> List[Dict[str, str]]:
    """Read and parse the input CSV file, converting dates to a standard format."""
    try:
        with open(input_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                try:
                    row['Run Date'] = datetime.strptime(row['Run Date'], '%m/%d/%Y').strftime('%Y%m%d')
                    data.append(row)
                except ValueError as e:
                    logger.warning(f"Skipping row with invalid date format: {row['Run Date']}")
            logger.info(f"Successfully read {len(data)} rows from {input_file}")
            return data
    except FileNotFoundError:
        logger.error(f"Input file {input_file} not found")
        raise
    except Exception as e:
        logger.error(f"Error reading {input_file}: {str(e)}")
        raise

def bucketize_to_account_and_ticker(data: List[Dict[str, str]]) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
    """Group data by account, ticker, and date."""
    buckets = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in data:
        account = row['Account Number']
        ticker = row['Symbol']
        rundate = row['Run Date']
        buckets[account][ticker][rundate].append(row)
    return buckets

def separate_closed_clusters(data: Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]) -> Tuple[Dict, Dict]:
    """Separate transactions into closed and open clusters based on quantity sum."""
    closed_clusters = defaultdict(lambda: defaultdict(dict))
    open_clusters = defaultdict(lambda: defaultdict(dict))

    for account in data:
        for ticker in data[account]:
            cluster = []
            quantity_sum = 0
            for rundate in sorted(data[account][ticker].keys()):
                for row in data[account][ticker][rundate]:
                    cluster.append(row)
                    quantity_sum += float(row['Quantity'] or 0)
                    if quantity_sum == 0:
                        cluster_add(closed_clusters, cluster, account, ticker, rundate)
                        cluster = []
                        quantity_sum = 0
            if cluster:
                cluster_add(open_clusters, cluster, account, ticker, rundate)

    return closed_clusters, open_clusters

def cluster_add(dest_dict: Dict, cluster: List[Dict[str, str]], account: str, ticker: str, rundate: str) -> None:
    """Add a cluster to the destination dictionary."""
    if ticker not in dest_dict[account][rundate]:
        dest_dict[account][rundate][ticker] = []
    dest_dict[account][rundate][ticker].append(cluster)

def write_clusters(clusters: Dict, filename: str) -> None:
    """Write clusters to a CSV file with calculated profit metrics, days, and average days for closed clusters."""
    headers = ['Account', 'Ticker', 'Date', 'Quantity', 'Price', 'Commission', 'Fees',
              'Amount', 'Profit', 'Profit%', 'Investment', 'Days', 'Average Days']

    try:
        total_profit = 0.0
        total_investment = 0.0
        cluster_days = []
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for account in sorted(clusters.keys()):
                for rundate in sorted(clusters[account].keys()):
                    for ticker in sorted(clusters[account][rundate].keys()):
                        writer.writerow([account, ticker, '', '', '', '', '', '', '', '', '', '', ''])
                        for cluster in clusters[account][rundate][ticker]:
                            calc_profit = filename != '_open.csv'
                            cluster_profit, cluster_investment, days = write_cluster(writer, cluster, calc_profit)
                            if calc_profit:
                                total_profit += cluster_profit
                                total_investment += cluster_investment
                                cluster_days.append(days)
                        writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', ''])

            if filename.endswith('_closed.csv') and total_investment != 0:
                total_profit_percentage = (total_profit / total_investment * 100)
                median_days = median(cluster_days) if cluster_days else 0
                average_days = mean(cluster_days) if cluster_days else 0
                writer.writerow(['Total', '', '', '', '', '', '', '', f'{total_profit:.2f}',
                               f'{total_profit_percentage:.2f} %', f'{total_investment:.2f}', f'{median_days:.2f}', f'{average_days:.2f}'])

        logger.info(f"Successfully wrote clusters to {filename}")
    except Exception as e:
        logger.error(f"Error writing to {filename}: {str(e)}")
        raise

def write_cluster(writer: csv.writer, cluster: List[Dict[str, str]], calculate_profit: bool) -> Tuple[float, float, int]:
    """Write a single cluster to the CSV file, calculating profit and days if needed."""
    buy_amount = 0
    sell_amount = 0
    total_quantity = 0
    dates = []

    for row in cluster:
        rundate = row['Run Date']
        quantity = float(row['Quantity'] or 0)
        price = float(row['Price ($)'] or 0)
        commission = float(row['Commission ($)'] or 0)
        fees = float(row['Fees ($)'] or 0)
        amount = float(row['Amount ($)'] or 0)

        total_quantity += quantity
        dates.append(rundate)
        writer.writerow(['', '', rundate, quantity, price, commission, fees, amount, '', '', '', '', ''])

        if amount < 0:
            buy_amount += amount
        else:
            sell_amount += amount

    profit = 0.0
    investment = 0.0
    days = 0
    if calculate_profit and total_quantity == 0:
        investment = -buy_amount
        profit = sell_amount - investment
        profit_percentage = (profit / investment * 100) if investment != 0 else 0
        # Calculate days as difference between max and min dates
        if dates:
            min_date = datetime.strptime(min(dates), '%Y%m%d')
            max_date = datetime.strptime(max(dates), '%Y%m%d')
            days = (max_date - min_date).days
        writer.writerow(['', '', '', '', '', '', '', '', f'{profit:.2f}',
                        f'{profit_percentage:.2f} %', f'{investment:.2f}', f'{days}', ''])

    return profit, investment, days

def filter_dates(clusters, date1, date2):
    retval = {}
    for account in clusters:
        for closingdate in clusters[account]:
            cd = int(closingdate)
            if cd >= date1 and cd <= date2:
                if account not in retval:
                    retval[account] = {}
                retval[account][closingdate] = clusters[account][closingdate]
    return retval

def main():
    """Main function to process input.csv and generate output CSV files."""
    try:
        data = read_data()
        bucketized_data = bucketize_to_account_and_ticker(data)
        closed_clusters, open_clusters = separate_closed_clusters(bucketized_data)
        write_clusters(closed_clusters, '_closed.csv')
        write_clusters(filter_dates(closed_clusters, 20250801, 20250831), '_august.csv')
        write_clusters(open_clusters, '_open.csv')
        logger.info("Processing completed successfully")
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()

