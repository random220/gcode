#include "base.h"
#include "algo.h"

void om(void) {
/*
TEFCRUxfT00xOgogICAgbGVmdCgpOwogICAgcmlnaHQoKTsKICAgIGxlZnQoKTsK
ICAgIGlmIChvbm1hcmsoKSkgewpMQUJFTF9PTTI6CiAgICAgICAgbGVmdCgpOwog
ICAgICAgIGdvdG8gTEFCRUxfT00yOwogICAgfQogICAgZ290byBMQUJFTF9PTTE7
Cg==
*/
}

void shivangi(void) {
/*
#   1. steps =1
#   2. left = steps
#   3. right = steps
#   4. if right >0:
#   5.      right()
#   6.      right--
#   7.      goto(4)
#   8. if onmark():
#   9.      goto(16)
#   10.if left>0:
#   11.     left()
#   12.     left--
#   13.     goto(10)
#   14. steps++
#   15. goto(2)
#   16. stop()
*/

    int STEPS;
    int LEFT;
    int RIGHT;

    STEPS = 1;
LABEL1:
    LEFT = STEPS;
    RIGHT = STEPS;
LABEL2:
    if (RIGHT >0) {
        right();
        RIGHT--;
        goto LABEL2;
    }
    if (onmark()) {
        goto LABEL4;
    }
LABEL3:
    if (LEFT>0) {
        left();
        LEFT--;
        goto LABEL3;
    }
    STEPS++;
    goto LABEL1;
LABEL4:
    stop();
}

