# genc -t x -d sample-transactions.tar.gpg.b64.banghostbangbang
# tar xf x/sample-transactions.tar.gpg.b64.banghostbangbang.plain
# rm -rf x

cat sample-transactions/*.csv | grep '^Run' | sort -u >a.csv
for f in sample-transactions/*.csv; do
    echo "$f"
    cat "$f" | egrep -v '^$' | egrep ' BOUGHT | SOLD ' >>a.csv
done
