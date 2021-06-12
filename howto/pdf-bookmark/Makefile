all:
	rm -rf .build; mkdir .build
	./cook-raw-index index-raw.txt >.build/index-cooked.txt
	./gen-indexmaker >.build/idxmaker.sh
	chmod a+x .build/idxmaker.sh
	(cd .build && ./idxmaker.sh repack)
	mv .build/a.txt .build/idxmaker-packed.txt

