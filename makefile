all:
	pyb analyze publish install

lint:
	pyb analyze

test:
	pyb run_integration_tests run_unit_tests

utest:
	pyb run_unit_tests

itest:
	pyb run_integration_tests

build:
	pyb

run:
	python src/main/scripts/run.py install
