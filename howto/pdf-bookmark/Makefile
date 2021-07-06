all:
	rm -rf .build; mkdir .build
	./saveindex.sh
	./unoffset index-raw.txt >.build/index-unoffsetted.txt
	./cook-raw-index-gs    .build/index-unoffsetted.txt >.build/index-cooked-gs.txt
	./cook-raw-index-pdftk .build/index-unoffsetted.txt >.build/index-cooked-pdftk.txt
	./gen-indexmaker >.build/idxmaker.sh
	chmod a+x .build/idxmaker.sh
	(cd .build && ./idxmaker.sh repack)
	mv .build/a.txt .build/idxmaker-packed.txt
	./add-index-with-pdftk.pl

