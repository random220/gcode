#!/bin/bash
echo '#!/bin/bash' >.build/a.txt
echo 'cat <<EOF|base64 -d|gunzip - >rawindex.txt' >>.build/a.txt
u=$(uname)
if [[ $u == Darwin ]]; then
    cat index-raw.txt | gzip -9 -|base64 -b 120 >>.build/a.txt
else
    cat index-raw.txt | gzip -9 -|base64 -w 120 >>.build/a.txt
fi
echo 'EOF' >>.build/a.txt
echo >>.build/a.txt
mv .build/a.txt .build/index-raw-base64.txt
