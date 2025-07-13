#include <stdio.h>
#include <stdlib.h>
#include "base.h"
#include "algo.h"

int G_T = 0;
int G_POS;

char s[80];

int main(int argc, char** argv) {
    char* e;
    e = getenv("POS");
    if (e == NULL) {
        sprintf(s, "POS=%d", LEFT_MARK);
        putenv(s);
        system("./sim");
        system("echo '----------------------------------'");
        sprintf(s, "POS=%d", RIGHT_MARK);
        putenv(s);
        system("./sim");
    }
    else {
        G_POS = atoi(e);
        print_position();
        //shivangi();
        om();
    }
    return 0;
}

void print_position(void) {
    printf("%d\t%d\n", G_T, G_POS);
}

void right(void) {
    G_POS++;
    G_T++;
    print_position();
    if (G_POS <= LEFT_MAX || G_POS >= RIGHT_MAX) {
        printf("Space maxed out\n");
        exit(0);
    }
    if (G_T >= T_MAX) {
        printf("Time maxed out\n");
        exit(0);
    }
}

void left(void) {
    G_POS--;
    G_T++;
    print_position();
    if (G_POS <= LEFT_MAX || G_POS >= RIGHT_MAX) {
        printf("Space maxed out\n");
        exit(0);
    }
    if (G_T >= T_MAX) {
        printf("Time maxed out\n");
        exit(0);
    }
}

void stop(void) {
}

int onmark(void) {
    if (G_POS == LEFT_MARK || G_POS == RIGHT_MARK) {
        return 1;
    }
    return 0;
}
