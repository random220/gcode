tk:
	rm -rf .build; mkdir .build
	./saveindex.sh
	./unoffset index-raw.txt >.build/index-unoffsetted.txt
	./cook-raw-index-gs    .build/index-unoffsetted.txt >.build/index-cooked-gs.txt
	./cook-raw-index-pdftk .build/index-unoffsetted.txt >.build/index-cooked-pdftk.txt
	./add-index-with-pdftk.pl

gs:
	rm -rf .build; mkdir .build
	./saveindex.sh
	./unoffset index-raw.txt >.build/index-unoffsetted.txt
	./cook-raw-index-gs    .build/index-unoffsetted.txt >.build/index-cooked-gs.txt
	./gen-indexmaker-gs >.build/idxmaker-gs.sh
	chmod a+x .build/idxmaker-gs.sh
	(cd .build && ./idxmaker-gs.sh repack)
	mv .build/a.txt .build/idxmaker-packed-gs.txt
	(cd .build && ./idxmaker-gs.sh idx)

