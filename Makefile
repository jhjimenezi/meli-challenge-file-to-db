start:
	docker-compose up

down:
	docker-compose down

hardown:
	docker-compose down -v

delete-images:
	docker rmi -f proccess-file-app
	docker rmi -f read-file-app