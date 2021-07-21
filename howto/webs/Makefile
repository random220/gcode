
all:
	./mkcont

deploy:
	docker cp server webs:/home/webs/bin/server
	docker exec webs bash -c 'chown -R webs:webs /home/webs'
	docker exec webs su - webs -c 'nohup ~/bin/server >/dev/null 2>&1 &'

