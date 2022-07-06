user:
	python manage.py createsuperuser --username=swasher --email=mr.swasher@gmail.com;

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations timer
