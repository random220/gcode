#!/usr/bin/perl
use strict;
use Data::Dumper;

=head aa
my $cmd = 'pdftk ~/in.pdf cat 1-10000 2>&1';
my @out = `$cmd`;
my $pages = 0;
for my $line (@out) {
    if ($line =~ m{input PDF has: (\d+) pages}) {
        $pages = $1;
    }
}
system "pdftk ~/in.pdf cat 1-$pages output ~/a.pdf";
=cut

if (!-f $ENV{HOME}.'/in.pdf') {
    die "Error: Cannot find ~/in.pdf\n";
}
system "pdftk ~/in.pdf cat output ~/a.pdf";
system 'pdftk ~/a.pdf dump_data output ~/a.txt';

my $home = $ENV{'HOME'};

open O, ">$home/b.txt" or die;

open F, "<$home/a.txt" or die;
while (my $line = <F>) {
    print O $line;
    if ($line =~ m{^NumberOfPages:\s+\d+\s*$}s) {
        last;
    }
}
open G, '<.build/index-cooked-pdftk.txt' or die;
while (my $line = <G>) {
    print O $line;
}
close G;

while (my $line = <F>) {
    print O $line;
}
close F;

close O;

system 'pdftk ~/a.pdf update_info ~/b.txt output ~/b.pdf';
