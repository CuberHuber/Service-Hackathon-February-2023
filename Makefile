
venv:
	poetry install

create-db: venv
	poetry run python create_db.py

docker-compose:
	docker-compose build
	docker-compose up

startup-new-db: create-db docker-compose

start: docker-compose
