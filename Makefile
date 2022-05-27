.PHONY : clean install dev test ui

VENV?=venv
PYTHON=${VENV}/bin/python

clean: # pdf, tex, and log files
	rm -f *.pdf *.tex *.log *.aux *.fls *.fdb_latexmk

install: . # in a virtual environment
	test -d $(VENV) || python -m venv $(VENV)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .

dev: requirements_dev.txt
	${PYTHON} -m pip install -r requirements_dev.txt

test: 
	${PYTHON} -m pytest

ui: qt5
	pyuic5 qt5/main.ui -o src/mathexpert/gui.py
	pyrcc5 qt5/media.qrc -o src/mathexpert/media_rc.py
