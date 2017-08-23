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

setup:
	python setup.py install

buildrun:
	pyb analyze publish install
	cd target/dist/Java-the-Hutts-1.0.dev0/ && python setup.py install
	cd src/main/scripts/ && python run.py
