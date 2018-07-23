while ($f = <DATA>) {
    chomp $f;
    $g = $f;
    $g =~ s/\%20/ /g;
    ($n, $g) = $g =~ m{^(\d+)\.(.+)$};
    ($n) = "00$n" =~ m{(..)$};
    $g = "$n-$g";
    print "mv '$f' '$g'\n";

}
__DATA__
