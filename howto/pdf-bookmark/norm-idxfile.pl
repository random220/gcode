#!/usr/bin/env perl
use strict;
my @l = ();
my $n = 0;

if (scalar @ARGV != 1) {
    print("Error: Need the index file name\n");
    exit 1;
}
my $infile = $ARGV[0];
if (! -f $infile) {
    print("Error: Need the index file name. \"$infile\" is not a file\n");
    exit 1;
}
open F, "<$infile" or die;
while (my $l = <F>) {
    $l =~ s{\s*$}{}s;
    if ($l =~ m{^(.+?)\s+(\d+\*?)$}) {
        my ($text, $num) = ($1, $2);
        if ($text =~ m{^\s*_offset\s*$}i) {
            $text = "_offset $num";
            $num = -1;
        }
        push @l, {'t' => $text, 'n' => $num};
        if ($n < length($text)) {
            $n = length($text);
        }
    }
    else {
        push @l, {'t' => $l, 'n' => -1};
    }
}
close F;

$n += 2;

for my $line (@l) {
    if ($line->{'n'} == -1) {
        print($line->{'t'}."\n");
    }
    else {
        printf("\%-${n}s\%s\n", $line->{'t'}, $line->{'n'})
    }
}
