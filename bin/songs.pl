while ($l = <DATA>) {
    chomp $l;
    $l =~ m{^(.+?)[\s\-]+(\d+)\:(\d+)$};
    $title = $1;
    $min = $2;
    $sec = $3;
    $x = 60 * $min + $sec;
    $x = $x.'.00000';
    print "$x\t$x\t$title\n";
}
__DATA__
Khal Nayak Hoon Main - 00:00
Choli Ke Peeche - 07:28
Palki Pe Hoke - 16:00
Aaja Sajan Aaja - 23:43
O Maa Tujhe Salam - 27:42
Aye Sahib Yeh Theek Nahin - 30:06
Choli Ke Peeche (Male) - 35:14
khal Nayak Hai Tu - 37:55
Aise Teri Yaad Aati Hai - 44:57
