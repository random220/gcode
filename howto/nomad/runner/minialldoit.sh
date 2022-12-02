#!/bin/bash

mkdir .xx
cd .xx


docker run -d -p 6000:5000 --restart always --name registry registry
tmux new-session -d -s mynomad bash -c 'nomad agent -dev'
# To attach to it
# tmux a -t mynomad

cat <<'EOF' | openssl enc -d -base64|tar xfz -
H4sIAM3PiWMCA+1XS4vbMBDO2b9i6j0nfskObNlLdym9pFsWeiilLIos22psy+iR
JS357x0/kk1amp4SGvB30KCZ0UhC+jSjB8lWXGWi5JOzwff9hBBo5TyJO+mHfb9D
EIYQkIiEUZSEPgFUJGE4AX9yAVhtqMKlyOq0H7pl2elNImAvrwTvnx4XYJe2NvY2
9Gc+ce4fP30BUeN+y3KmC/Ccp88fwXvV9B68NmrT2+8XD+Dt+s5kxBXh9VjPyv95
HJ/gP4kG/odzQoKO/yQa+X8J3LzxlqL2lhSZ69DGTHNuYLoB26TU8ENNKrSZ2iZX
ND3SDzcI1qICZlUJuTCgbSqh5oZRMz4I/zN2z/Y55/gn/zHnD/k/JnGX/7ESGPl/
cf5zVkgoxB/ypcD6EIyy/C2k0gHQJecNBE4qa+6MBL9iKFvXXM1qWdH0rPW//3f+
J1G8r/+DsM3/UZCQkf+XwHe5BLe/BC78RGpj2qcMswJXGu7gq5uywP2GerNpOCpc
zdVaMO6iKlfSNsejAZjEvwQ6Rl0PS4AXqVaDbdu1Q4RBhz606iIPcQZto+RapFy1
lu52ugchDNWr3yfGpSux7gek3a92F4rJOhP53g1AVDTvpiwlo2UhtblN8NC84xUA
UGuKZy0z85xRUeKA9gkcrNtBKq6lVYzrg/issa24gxhvwk3XLj782JsrXkm1QXMY
J2jGdvHuKGrbbp3t+LCOGDHinPgFXEff8AAUAAA=
EOF

docker build -t runner .
docker tag runner localhost:6000/runner
docker push localhost:6000/runner
nomad job run runner.nomad

