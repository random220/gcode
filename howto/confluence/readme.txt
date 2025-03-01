https://confluence.atlassian.com/doc/confluence-installation-guide-135681.html
https://confluence.atlassian.com/doc/install-a-confluence-data-center-trial-838416249.html
https://www.atlassian.com/software/confluence/download-archives
https://confluence.atlassian.com/doc/confluence-installation-and-upgrade-guide-214864161.html


docker network create om
docker volume create confluence

docker rm -f postgres
docker run -itd --network om \
    --name postgres -h postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    postgres

#docker exec -it -u postgres postgres bash
#   psql

docker exec -it postgres bash
    psql -U postgres
        CREATE USER confluence WITH PASSWORD 'confluence' SUPERUSER;
        #drop user confluence;
        CREATE DATABASE confluence;


docker run -itd --network om \
    --name confluence -h confluence \
    -v confluence:/var/atlassian/application-data/confluence \
    -p 8090:8090 -p 8091:8091 \
    atlassian/confluence:8.9.4-ubuntu-jdk17


http://localhost:8090
Hostname postgress
Port 5432
User confluence
password confluence
database confluence



