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
	rm -rf core/migrations/*
	rm -rf orders/migrations/*
	rm -rf stanzforms/migrations/*
	rm -rf warehouse/migrations/*
	docker compose down
	docker volume prune --force
	docker compose up -d
	sleep 2
	python manage.py makemigrations core orders stanzforms warehouse
	python manage.py migrate --run-syncdb
	python manage.py loaddata */fixtures/*.json
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com;

fixtures:
	python -Xutf8 manage.py dumpdata core.papersize --indent 4 --output core/fixtures/papersize.json
	python -Xutf8 manage.py dumpdata core.paper --indent 4 --output core/fixtures/paper.json
	python -Xutf8 manage.py dumpdata core.customer --indent 4 --output core/fixtures/customer.json
	python -Xutf8 manage.py dumpdata core.PrintingPress --indent 4 --output core/fixtures/PrintingPress.json
	python -Xutf8 manage.py dumpdata core.Customer --indent 4 --output core/fixtures/Customer.json
	python -Xutf8 manage.py dumpdata core.Customer --indent 4 --output core/fixtures/Contractor.json
	python -Xutf8 manage.py dumpdata auth.User --indent 4 --output printMES/fixtures/User.json
	python -Xutf8 manage.py dumpdata auth.Group --indent 4  --output printMES/fixtures/Group.json
	python -Xutf8 manage.py dumpdata auth.Group_permissions --indent 4  --output printMES/fixtures/Group_permissions.json


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

heroku-reset-db:
	heroku pg:reset
	heroku run python manage.py migrate
	heroku run python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com
	heroku run python manage.py collectstatic