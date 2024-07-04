all: sim

sim: base.o algo.o
	gcc -o sim base.o algo.o

base.o: base.c
	gcc -c base.c

algo.o: algo.c
	gcc -c algo.c

clean:
	rm -f base.o algo.o sim
