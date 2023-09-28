DIST_DIR := dist

default: clean sdist

clean:
	rm -rf $(DIST_DIR)/*

sdist:
	python3 setup.py sdist

testupload:
	twine upload dist/* -r testpypi

upload:
	twine upload dist/*
