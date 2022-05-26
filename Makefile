.PHONY : clean install test

VENV?=venv
PYTHON=${VENV}/bin/python

clean: # pdf, tex, and log files
	rm -f *.pdf *.tex *.log

install: . # in a virtual environment
	test -d $(VENV) || python -m venv $(VENV)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .

test: requirements_dev.txt
	${PYTHON} -m pip install -r requirements_dev.txt
	${PYTHON} -m pytest
