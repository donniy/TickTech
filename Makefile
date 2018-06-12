install:
	npm install --prefix app/frontend
	. venv/bin/activate; \
	pip3 install -r requirements.txt

build:
	npm run build --prefix app/frontend

run-flask:
	. venv/bin/activate; \
	export FLASK_ENV=development; \
	./.db_credentials; \
	FLASK_APP=app/backend/flaskr python3 -m flask run

run-vue:
	npm run dev --prefix app/frontend
