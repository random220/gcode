r:      r.c stow.pl Makefile instructions.txt
	uname -a >uname.txt
	perl stow.pl r.c Makefile stow.pl instructions.txt uname.txt >code.c
	#gcc -static -o r r.c code.c
	gcc -o r r.c code.c
	strip r
	cat instructions.txt

clean:
	rm -f code.c r
