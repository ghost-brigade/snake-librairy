init:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	python3 manage.py runserver


migrate:
	python3 manage.py migrate

migration:
	python3 manage.py makemigrations