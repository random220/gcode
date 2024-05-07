#!/usr/bin/env python3
import os
import sys

LEFT_MAX  = -100;
RIGHT_MAX = 100;
T_MAX = 1000;

LEFT_MARK  = -2;
RIGHT_MARK = 3;

G = {};
G['T'] = 0;

def main():
    if not 'POS' in os.environ:
        os.environ['POS'] = str(LEFT_MARK)
        os.system(sys.argv[0])
        print("-------------------------------------")
        os.environ['POS'] = str(RIGHT_MARK)
        os.system(sys.argv[0])
    else:
        G['POS'] = os.environ.get('POS')
        print_position();
        shivangi();
        #om();

def om():
    pass
    '''
    cat <<EOF | base64 -d
    TEFCRUwxOgogICAgbW92ZV9sZWZ0KCk7CiAgICBtb3ZlX3JpZ2h0KCk7CiAgICBt
    b3ZlX2xlZnQoKTsKICAgIGlmIChvbm1hcmsoKSkgewpMQUJFTDI6CiAgICAgICAg
    bW92ZV9sZWZ0KCk7CiAgICAgICAgZ290byBMQUJFTDI7CiAgICB9CiAgICBnb3Rv
    IExBQkVMMTsK
    EOF
    '''

def shivangi():
    pass
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

    '''
    $steps = 1;
LABEL1:
    $left = $steps;
    $right = $steps;
LABEL2:
    if ($right >0) {
        move_right();
        $right--;
        goto LABEL2;
    }
    if (onmark()) {
        goto LABEL4;
    }
LABEL3:
    if ($left>0) {
        move_left();
        $left--;
        goto LABEL3;
    }
    $steps++;
    goto LABEL1;
LABEL4:
    stop();
    '''

def print_position():
    print(str(G['T']) + "\t" + str(G['POS']))

def move_right():
    G['POS'] += 1
    G['T'] += 1
    print_position()
    if G['POS'] <= LEFT_MAX or G['POS'] >= RIGHT_MAX:
        print("Space maxed out")
        sys.exit(0)

    if G['T'] >= T_MAX:
        print("Time maxed out")
        sys.exit(0)


def move_left():
    G['POS'] -= 1
    G['T'] += 1
    print_position()
    if G['POS'] <= LEFT_MAX or G['POS'] >= RIGHT_MAX:
        print("Space maxed out")
        sys.exit(0)

    if G['T'] >= T_MAX:
        print("Time maxed out")
        sys.exit(0)

def stop():
    return

def onmark():
    if G['POS'] == LEFT_MARK or G['POS'] == RIGHT_MARK:
        return True
    return False


main()
