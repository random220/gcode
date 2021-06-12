#!/usr/bin/perl
use strict;
use Data::Dumper;

open F, "<index-raw-all.txt" or die;

while (my $line = <F>) {
    $line =~ s{\s*$}{}s;
    if ($line =~ m{^\s*$}) {
        print "\n";
        next;
    }
    if ($line =~ m{^(.*)\s+(\d+)$}) {
        my $page = $2;
        $page += 18;
        $line .= " $page";
    }
    else {
        $line .= " 1";
    }

    print "$line\n";
}
close F;
