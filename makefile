clean:
	rm -rf dist/
	rm -rf build/
build:
	venv/bin/pyinstaller --one-file wol.py

install:
	cp dist/wol ~/.scripts
	chmod +x ~/.scripts/wol
