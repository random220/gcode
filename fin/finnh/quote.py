#!/usr/bin/env python

import os, sys
import finnhub


def get_API_key():
    try:
        keyfile = os.environ['HOME']+'/.ssh/apikey/finn'
        with open(keyfile, 'rt') as f:
            key = f.readline().strip()
    except:
        print(f"Error: Need {keyfile}")
        sys.exit(1)
    return key

if __name__ == "__main__":
    api_key = get_API_key()
    finnhub_client = finnhub.Client(api_key=api_key)
    print(finnhub_client.quote('AAPL'))
