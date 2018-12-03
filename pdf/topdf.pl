#!/usr/bin/perl
use strict;
my @xcf_files = `ls -1 *.xcf`;
# 000.jpg:           JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, progressive, precision 8, 594x693, frames 3
# page_0000.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2373x3142, frames 3
# page_0001.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2373x3159, frames 3
# page_0002.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2356x3197, frames 3
# page_0003.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2351x3170, frames 3
# page_0004.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2174x3180, frames 3
# page_0005.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2339x3110, frames 3
# page_0006.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2346x3180, frames 3
# page_0007.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2352x3164, frames 3
# page_0008.xcf.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 2395x3197, frames 3

my $join_cmd = "gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished.pdf \\\n";

for my $xcf_file (@xcf_files) {
    chomp $xcf_file;
    my $jpg_file = $xcf_file;
    $jpg_file =~ s{\.xcf}{.jpg};
    print "convert -density 300 -quality 80 $xcf_file $jpg_file\n";

    # 000.jpg:           JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, progressive, precision 8, 594x693, frames 3
    if ($line =~ m{^([^\:]+\.jpg)\:\s+JPEG image data.*, density (\d+)x(\d+).+precision 8, (\d+)x(\d+)}) {
        my ($f, $density_x, $density_y, $x, $y) = ($1, $2, $3, $4, $5);
        if ($density_x != $density_y) {
            print "==> density error: $line";
            next;
        }
        # my $x_inch = $x / $density_x;
        # my $y_inch = $y / $density_y;
        my $x_inch = $x / 300;
        my $y_inch = $y / 300;
        $join_cmd .= "    $f.pdf \\\n";
        my $cmd = "img2pdf -o $f.pdf --imgsize=${x_inch}inx${y_inch}in --pagesize=Letter $f";
        print "$cmd\n";
    }
}

print "$join_cmd\n";

