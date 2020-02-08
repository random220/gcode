
use strict;

my $pid;
die "Can't fork: $!\n" unless defined($pid = open(KID, '-|'));
if ($pid) { # parent
    while (my $l = <KID>) {
        print localtime(time).'  ';
        print $l;
    }
    close KID;
}
else { # kid
    my $n = 0;
    open(OLDERR, ">&STDERR");
    open STDERR, '>&STDOUT';
    print STDOUT "out\n";
    print STDERR "err\n";
    print "hi\n";
    close(STDERR);
    open(STDERR, ">&OLDERR");
}

if ($pid) { # parent
    while (my $l = <KID>) {
        print localtime(time).'  ';
        print $l;
    }
    close KID;
}
else { # kid
    my $n = 0;
    #open STDERR, '>&STDOUT';
    print STDOUT "out\n";
    print STDERR "err\n";
}
