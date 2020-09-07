./dist/esort: ./dist/exifsort
	staticx ./dist/exifsort ./dist/esort

./dist/exifsort: exifsort.py
	pyinstaller -F -s exifsort.py

clean:
	rm -rf dist build exifsort.spec
