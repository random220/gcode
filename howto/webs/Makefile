# https://pypi.org/project/websockets/

all:
	./mkcont

deploy-py:
	docker stop webs; docker start webs
	docker cp server.py webs:/home/webs/bin/server.py
	docker exec webs bash -c 'chown -R webs:webs /home/webs'
	docker exec webs su - webs -c 'nohup ~/bin/server.py >/dev/null 2>&1 &'

deploy-js:
	docker stop webs; docker start webs
	docker cp server.js webs:/home/webs/bin/server.js
	docker exec webs bash -c 'cd /home/webs/bin; npm init -y -f; npm install ws'
	docker exec webs bash -c 'chown -R webs:webs /home/webs'
	docker exec webs su - webs -c 'nohup ~/bin/server.js >/dev/null 2>&1 &'

py:
	make deploy-py
js:
	make deploy-js
