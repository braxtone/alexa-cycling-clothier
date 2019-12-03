VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate:
	test -d venv || virtualenv -p python3 venv
	${PYTHON} -m pip install --quiet -r requirements.txt
	touch venv/bin/activate

install_dev: venv
	${PYTHON} -m pip install --quiet -r requirements_dev.txt

npm_install: install_dev
	npm install

clean:
	source venv/bin/activate; deactivate
	rm -rf venv
	find . -name '*.pyc' -exec rm --f {} +
	find . -name '*.pyo' -exec rm --f {} +

lint: install_dev
	${PYTHON} -m flake8 handler.py cyclingclothier

test: lint 
	${PYTHON} -m pytest

local: npm_install 
	$(VENV_ACTIVATE); sls invoke local \
		--function CyclingClothier \
		--path tests/input.json \
		--stage local \
		--env DARKSKY_API_KEY=$(DARKSKY_API_KEY)

deploy_dev: test
	$(VENV_ACTIVATE); sls deploy \
		--stage dev

