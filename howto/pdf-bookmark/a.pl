while ($l = <>) {
    chomp $l;
    if ($l =~ m{^(.*)\s(\d+)\s*$}) {
        ($x, $y) = ($1, $2);
        if ($y > 1282) {
            $y -= 45;
        }
        print "$x $y\n";
    }
    else {
        print "$l\n";
    }
}
