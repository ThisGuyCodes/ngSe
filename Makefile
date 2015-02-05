SUPPORTED_PYTHON=$(shell python --version 2>&1|cut -f2 -d' '|cut -f1,2 -d.)

all: source wheel

clean:
	rm -r dist build ngSe.egg-info || true

source: clean
	python setup.py sdist

wheel: clean
	python setup.py bdist_wheel --python-tag $(SUPPORTED_PYTHON)

upload: source wheel
	@read -p "Are you sure you want to upload to PyPi? " -n 1 -r REPLY;\
	echo;\
	if [ "$$REPLY" == "y" ];\
	then\
		twine upload dist/* --sign;\
	fi
