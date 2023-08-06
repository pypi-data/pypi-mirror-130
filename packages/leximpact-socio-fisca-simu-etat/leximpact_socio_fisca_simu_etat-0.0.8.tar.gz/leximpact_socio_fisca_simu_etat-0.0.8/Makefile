############
### Makefile for NBDev (leximpact_socio_fisca_simu_etat)
############

# to exit at first error, remove .ONESHELL:

SHELL := /bin/bash
SRC = $(wildcard notebooks/*.ipynb)

all: leximpact-socio-fiscal-simu-etat docs

leximpact-socio-fiscal-simu-etat: $(SRC)
	poetry run nbdev_build_lib
	touch leximpact-socio-fiscal-simu-etat

install:
	poetry install
	poetry run python -m ipykernel install --name leximpact-socio-fiscal-simu-etat-kernel --user
	poetry run pre-commit install

api:
	poetry run api

precommit:
	-poetry run pre-commit run --all-files
	-$(MAKE) lib
	-poetry run pre-commit run --all-files
	-echo "XXXXXXXX Last check XXXXXXXXXXX"
	-poetry run pre-commit run --all-files

lib:
	poetry run nbdev_build_lib
	#poetry run nbdev_build_lib --fname notebooks/retraitement_erfs-fpr/0401_db_add_var_copules-algo_monte-carlo.ipynb
	#find ./notebooks/ -name '*.ipynb' -exec poetry run nbdev_build_lib --fname \{\} \;

doc:
	poetry run nbdev_build_docs
	#find ./notebooks/ -name '*.ipynb' -exec poetry run nbdev_build_docs --fname \{\} \;


sync:
	poetry run nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	poetry run nbdev_build_docs
	touch docs

test:
	poetry run pytest
	# poetry run nbdev_test_nbs
	# poetry run pytest -s tests/test_jwt.py -k test_check_error_token_malformed

test-nb:
	poetry run papermill --execution-timeout 300 notebooks/aggregates_build.ipynb ./papermill/aggregates_build-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/aggregates_read.ipynb ./papermill/aggregates_read-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/cache.ipynb ./papermill/cache-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/schema.ipynb ./papermill/schema-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/config.ipynb ./papermill/config-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/logger.ipynb ./papermill/logger-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/test_openfisca.ipynb ./papermill/test_openfisca-paper.ipynb
	poetry run papermill --execution-timeout 300 notebooks/simu_budget.ipynb ./papermill/simu_budget-paper.ipynb

release: pypi conda_release
	poetry run nbdev_bump_version

conda_release:
	poetry run fastrelease_conda_package

pypi: dist
	poetry run twine upload --repository pypi dist/*

dist: clean
	poetry run python setup.py sdist bdist_wheel

clean:
	rm -rf dist
	rm -rf leximpact_socio_fisca_simu_etat.egg-info
	rm -rf papermill
