## Ref
- [Installing] (https://beancount.github.io/docs/installing_beancount.html)
- [Getting Started] (https://beancount.github.io/docs/getting_started_with_beancount.html)
- [Youtube Intro] (https://www.youtube.com/watch?v=g1oma2cO61k)
- https://beancount.io/docs/Solutions/scriptable-workflows

## Install
```
cd ~/sb
mkdir bean
cd bean
python -m venv e
. e/bin/activate
pip install -U pip
pip install fava        # The web interface AND beancount too
```

## Test installation
1. create a simple beancount ledger, and save to file tst.bean

 ```
 cat <<EOF >tst.bean
 2014-01-01 open Assets:Checking
 2014-01-01 open Equity:Opening-Balances

 2014-01-02 * "Deposit"
      Assets:Checking           100.00 USD
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
 beanquery> .exit
 ```

3. Alternatively, check what a full fledged accouting file looks like

  ```
  bean-example --help
  bean-example >example.bean
  fava example.bean
  ```
  
 ## Using beancount
 
 Ref: https://beancount.github.io/docs/getting_started_with_beancount.html
 
 