VENV?=venv
PYTHON=${VENV}/bin/python

clean: # pdf, tex, and log files
	rm -f *.pdf *.tex *.log

install: requirements.txt # in a virtual environment
	test -d $(VENV) || python -m venv $(VENV)
	${PYTHON} -m pip install -vU pip
	${PYTHON} -m pip install -vr requirements.txt
	touch $(VENV)/bin/activate
