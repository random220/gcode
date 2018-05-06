#!/usr/bin/perl
use strict;

my @questions;
my @answers;
my ($left, $middle);
my $n = 0;
while ($n <100) {
    $left = int(rand(10));
    next if($left == 0);
    $middle = int(rand(1000));
    next if($left > $middle);
    $n++;
    push @questions, "   $n.            $left)$middle\n\n\n\n\n\n";
    my $ans = int($middle / $left);
    my $R = $middle % $left;
    push @answers, "    $n - $ans R $R\n";
}


open F, ">q.txt" or die;
print F join '', @questions;
close F;
open F, ">a.txt" or die;
print F join '', @answers;
close F;
