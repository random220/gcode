#!/bin/bash

docker rm -f pgadmin postgres
rm -rf $HOME/.pgdata


docker network create pg
docker run -d \
    --network=pg \
    --name=postgres \
    -h postgres \
    -e POSTGRES_PASSWORD=secret \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $HOME/.pgdata:/var/lib/postgresql/data \
    postgres
    #-p 5432:5432 \

docker run -d \
    --network=pg \
    --name=pgadmin \
    -h pgadmin \
    -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=root@crondite.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=secretadmin' \
    dpage/pgadmin4


cat <<'EOF'




# http://localhost:80
# root@crondite.com / secretadmin
#
# Connection Parameters
# Host name/address: postgres
# Port: 5432
# Maintenance database: postgres
# Username: postgres
EOF
