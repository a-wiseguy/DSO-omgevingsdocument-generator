.DEFAULT_GOAL := help
default: help;
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


DIR ?= ../../output
generate:
	@python app/cmds.py xsd-all $(DIR)

pip-sync:
	pip install -U pip pip-tools
	pip-sync requirements.txt requirements-dev.txt

pip-compile:
	pip install -U pip pip-tools
	pip-compile requirements.in
	pip-compile requirements-dev.in

pip-upgrade:
	pip install -U pip pip-tools
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements-dev.in

fix:
	python -m isort app/
	python -m black app/ stubs/
	python -m autoflake -ri --exclude=__init__.py --remove-all-unused-imports app/ stubs/

check-security:
	python -m bandit --configfile bandit.yml -r app/

check-venture:
	python -m vulture app/ --exclude app/tests/ --min-confidence 100

check: check-venture check-security
