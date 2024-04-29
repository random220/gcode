#!/usr/bin/perl

$LEFT_MAX  = -100;
$RIGHT_MAX = 100;
$T_MAX = 1000;

$LEFT_MARK  = -2;
$RIGHT_MARK = 3;

$G = {};
$G->{T} = 0;

if (! exists $ENV{'POS'}) {
    $ENV{'POS'} = $LEFT_MARK;
    system("perl $0");
    print("-------------------------------------\n");
    $ENV{'POS'} = $RIGHT_MARK;
    system("perl $0");
}
else{
    $G->{POS} = $ENV{'POS'};
    print_position();
    shivangi();
    #om();
}

sub om() {
=head omcode
cat <<EOF | base64 -d
TEFCRUwxOgogICAgbW92ZV9sZWZ0KCk7CiAgICBtb3ZlX3JpZ2h0KCk7CiAgICBt
b3ZlX2xlZnQoKTsKICAgIGlmIChvbm1hcmsoKSkgewpMQUJFTDI6CiAgICAgICAg
bW92ZV9sZWZ0KCk7CiAgICAgICAgZ290byBMQUJFTDI7CiAgICB9CiAgICBnb3Rv
IExBQkVMMTsK
EOF
=cut
}

sub shivangi() {
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
}

sub print_position() {
    print($G->{T} . "\t"  . $G->{POS} . "\n");
}

sub move_right() {
    $G->{POS}++;
    $G->{T}++;
    print_position();
    if ($G->{POS} <= $LEFT_MAX || $G->{POS} >= $RIGHT_MAX) {
        printf("Space maxed out\n");
        exit(0);
    }
    if ($G->{T} >= $T_MAX) {
        printf("Time maxed out\n");
        exit(0);
    }
}
sub move_left() {
    $G->{POS}--;
    $G->{T}++;
    print_position();
    if ($G->{POS} <= $LEFT_MAX || $G->{POS} >= $RIGHT_MAX) {
        printf("Space maxed out\n");
        exit(0);
    }
    if ($G->{T} >= $T_MAX) {
        printf("Time maxed out\n");
        exit(0);
    }
}

sub stop() {
    return;
}

sub onmark() {
    if ($G->{POS} == $LEFT_MARK or $G->{POS} == $RIGHT_MARK) {
        return 1;
    }
    return 0;
}
