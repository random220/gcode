## Ref
https://beancount.github.io/docs/installing_beancount.html

## Install
```
cd ~/sb
mkdir bean
cd bean
python -m venv e
. e/bin/activate
pip install -U pip
#pip install pipx
#pipx install beancount
#pip install beancount
pip install beanquery
```

## Test installation
1. create a simple beancount ledger, and save to file tst.bean

 ```
 cat <<EOF >tst.bean
 2024-01-01 open Assets:Bank
 2024-01-01 open Equity:Opening-Balances
 2024-01-01 * "Opening Balance"
      Assets:Bank  1000.00 USD
      Equity:Opening-Balances
 EOF
 ```

2. Then run

 ```
 bean-query tst.bean
 ```

3. Confirm, that you get prompt like that

 ```
 Input file: "Beancount"
 Ready with 3 directives (2 postings in 1 transactions, 0 validation errors)
 beanquery> exit
 ```
 
 ## Using beancount
 
 Ref: https://beancount.github.io/docs/getting_started_with_beancount.html
 
 