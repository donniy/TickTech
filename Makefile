install:
	export NVM_DIR="$HOME/.nvm";\
	npm install --prefix app/frontend
	. venv/bin/activate; \
	pip3 install -r requirements.txt

build:
	export NVM_DIR="$HOME/.nvm";\
	npm run build --prefix app/frontend

run-flask:
	. venv/bin/activate; \
	export FLASK_ENV=development; \
	./.db_credentials; \
	FLASK_APP=app/backend/flaskr python3 -m flask run

run-vue:
	export NVM_DIR="$HOME/.nvm";
	npm run dev --prefix app/frontend

test-backend:
	. venv/bin/activate; \
	cd app/backend/flaskr; \
	python3 -m pytest

test-frontend:
	export NVM_DIR="$HOME/.nvm"; \
	npm run test --prefix app/frontend

test: 	test-frontend test-backend
