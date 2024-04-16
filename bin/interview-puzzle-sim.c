#include <stdio.h>
#include <stdlib.h>


int LEFT_MAX  = -100;
int RIGHT_MAX = 100;
int T_MAX = 1000;

int LEFT_MARK  = -2;
int RIGHT_MARK = 3;

int G_T = 0;
int G_POS;

char s[80];

void om(void);
void shivangi(void);
void print_position(void);
void move_right(void);
void move_left(void);
void stop(void);
int onmark(void);

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
        shivangi();
        //om();
    }
    return 0;
}

void om(void) {
/*
TEFCRUxfT00xOgogICAgbW92ZV9sZWZ0KCk7CiAgICBtb3ZlX3JpZ2h0KCk7CiAg
ICBtb3ZlX2xlZnQoKTsKICAgIGlmIChvbm1hcmsoKSkgewpMQUJFTF9PTTI6CiAg
ICAgICAgbW92ZV9sZWZ0KCk7CiAgICAgICAgZ290byBMQUJFTF9PTTI7CiAgICB9
CiAgICBnb3RvIExBQkVMX09NMTsK
*/
}

void shivangi(void) {
/*
#   1. steps =1
#   2. left = steps
#   3. right = steps
#   4. if right >0:
#   5.      move_right()
#   6.      right--
#   7.      goto(4)
#   8. if onmark():
#   9.      goto(16)
#   10.if left>0:
#   11.     move_left()
#   12.     left--
#   13.     goto(10)
#   14. steps++
#   15. goto(2)
#   16. stop()
*/

    int steps;
    int left;
    int right;

    steps = 1;
LABEL1:
    left = steps;
    right = steps;
LABEL2:
    if (right >0) {
        move_right();
        right--;
        goto LABEL2;
    }
    if (onmark()) {
        goto LABEL4;
    }
LABEL3:
    if (left>0) {
        move_left();
        left--;
        goto LABEL3;
    }
    steps++;
    goto LABEL1;
LABEL4:
    stop();
}

void print_position(void) {
    printf("%d\t%d\n", G_T, G_POS);
}

void move_right(void) {
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

void move_left(void) {
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
