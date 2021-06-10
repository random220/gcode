$n = 0;
while ($l = <DATA>) {
    $l0 = $l;
    $n++;
    $l =~ s{\s*$}{};
    if ($l =~ m{^\s*$}s) {
        print("\n");
    }
    elsif ($l =~ m{^(\s*)(.+)\s+(\d+)$}s) {
        ($space, $title, $pagenum) = ($1, $2, $3);
        print("$space\[/Page $pagenum /Title ($title) /OUT pdfmark\n");
    }
    else {
        print("BADLINE $n : $l0");
    }
}
__DATA__
1 Basic Concepts of Algebra 18
    The Language of Algebra 19
        1-1 Real Numbers and Their Graphs 1 19
        1-2 Simplifying Expressions 6 100

    Operating with Real Numbers 100
        1-3 Basic Properties of Real Numbers 14 100
        1-4 Sums and Differences 21 100
        1-5 Products 27 100
        1-6 Quotients 33 100

    Solving Equations and Solving Problems 100
        1-7 Solving Equations in One Variable 37 100
        1-8 Words into Symbols 43 100
        1-9 Problem Solving with Equations 49 100

* Explorations: Exploring Irrational Numbers 832 100
* Technology 100
    Computer Exercises 100
        Page 5 100
        Page 32 100
    Calculator Key-In 12 100
* Special Topics 100
    Reading Algebra 100
        Page xiv 100
        Page 26 100
    Logical Symbols: Quantifiers 20 100
    Biographical Note 32 100
    Historical Note 42 100
    Challenge 48 100
* Reviews and Tests 100
    Mixed Review Exercises 100
        Page 5 100
        Page 20 100
        Page 31 100
        Page 42 100
        Page 54 100
    Self-Tests 100
        Page 13 100
        Page 36 100
        Page 54 100
    Chapter Summary 55 100
    Chapter Review 55 100
    Chapter Test 57 100

2 Inequalities and Proof 100
    Working with Inequalities 100
        2-1 Solving Inequalities in One Variable 59 100
        2-2 Solving Combined Inequalities 65 100
        2-3 Problem Solving Using Inequalities 69 100
    Working with Absolute Value 100
        2-4 Absolute Value in Open Sentences 73 100
        2-5 Solving Absolute Value Sentences Graphically 76 100
    Proving Theorems 100
        2-6 Theorems and Proofs 81 100
        2-7 Theorems about Order and Absolute Value 88 100
