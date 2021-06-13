all:
	rm -rf .build; mkdir .build
	./saveindex.sh
	./cook-raw-index-gs    index-raw.txt >.build/index-cooked-gs.txt
	./cook-raw-index-pdftk index-raw.txt >.build/index-cooked-pdftk.txt
	./gen-indexmaker >.build/idxmaker.sh
	chmod a+x .build/idxmaker.sh
	(cd .build && ./idxmaker.sh repack)
	mv .build/a.txt .build/idxmaker-packed.txt

