dummy:
	@echo Dont run without arguments!

admin:
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com --skip-checks;

migrations:
	# возможно тут надо указать имена apps после makemigrations
	python manage.py makemigrations

migrate:
	# нужно указывать --run-syncdb для первой миграции, иначе не создаются базы
	python manage.py migrate





cleardb:
	docker compose down
	docker volume prune --force
	docker compose up -d
	sleep 3
	python manage.py makemigrations core orders stanzforms warehouse
	python manage.py migrate --run-syncdb
	python manage.py loaddata --app core papersize.json
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com;

make_fixtures_core_papersize:
	python manage.py dumpdata core.papersize --indent 4 --output core/fixtures/papersize.json

make_fixtures_core_paper:
	python manage.py dumpdata core.paper --indent 4 --output core/fixtures/paper.json

make_fixtures_core_customers:
	python manage.py dumpdata core.customer --indent 4 --output core/fixtures/customer.json

make_fixtures_core_PrintingPress:
	python manage.py dumpdata core.PrintingPress --indent 4 --output core/fixtures/PrintingPress.json

make_fixtures_core_Customer:
	python manage.py dumpdata core.Customer --indent 4 --output core/fixtures/Customer.json

build:
	docker compose up -d  --build

up:
	docker compose up -d

down:
	docker compose down

make_requirements:
	pipenv run pip freeze > requirements.txt

ssh:
	docker exec -it sandglass_db_1 bash

