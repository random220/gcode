#!/usr/bin/perl
use strict;
use Data::Dumper;

my $pattern1 = 'dd-d*dd/d+dd/d-dd+ddd';
my $pattern2 = 'dd-dd/d*d+dd/d-dd+ddd';
my $pattern3 = 'd*(dd+d)-[(dd+dd)/{(dd-d)*(dd-d)}]';
my $pattern4 = '{(dd-d)*(dd+d)-(dd-d)}/{(dd-d)-(dd-d)}*(ddd+dd)*(dd-dd)';
my ($html_header, $html_footer);

set_header_footer(\$html_header, \$html_footer);
print $html_header;
do_pattern($pattern1, 10);
do_pattern($pattern2, 10);
print $html_footer;
# my @patterns = `cat a.txt`;
# for my $p (@patterns) {
#     chomp $p;
#     do_pattern($p, 1);
# }


sub do_pattern
{
    my ($pattern, $num) = @_;
    my $line = 0;
    while ($num != 0) {
        my @p = split //, $pattern;
        my $expr   = '';
        for my $d (@p) {
            if ($d eq 'd') {
                $d = int(rand(10));
                $expr   .= $d;
            }
            elsif ($d =~ /^\d$/ or $d eq ' ') {
                $expr   .= $d;
            }
            elsif($d eq '*') {
                $expr   .= '*';
            }
            elsif($d eq chr(0xd7)) {
                $expr   .= '*';
            }
            elsif($d eq chr(0xf7)) {
                $expr   .= '/';
            }
            elsif($d eq '/') {
                $expr   .= '/';
            }
            elsif($d eq '+' or $d eq '-') {
                $expr   .= $d;
            }
            elsif($d eq '(' or $d eq '{' or $d eq '[') {
                $expr   .= '(';
            }
            elsif($d eq ')' or $d eq '}' or $d eq ']') {
                $expr   .= ')';
            }
        }
        $expr = sanitize_expr($expr);
        my $string = expr_to_string($expr);
        $expr = rmzero_expr($expr);
        my $result = 0;

        my $expr = '$result = '.$expr;
        eval $expr;
        chomp $@;
        if ($@ eq '' and ($result < -1 or 1 < $result)) {
            $line++;
            printf('%02d%s %s = %d'."<br><br><br><br>\n", $line, '&nbsp;&nbsp;&nbsp;', $string, $result);
            $num--;
        }
    }
}

sub expr_to_string
{
    my ($expr) = @_;
    my $divide = '&divide;';
    my $multiply = '&times;';
    $expr =~ s{/}{$divide}g;
    $expr =~ s{\*}{$multiply}g;
    return $expr;
}

sub sanitize_expr
{
    my ($expr) = @_;
    $expr =~ s/ //g;
    my ($left, $right);
    $right = $expr;
    while ($right =~ m{^(.*?)(\d+)/(\d+)(.*)$}) {
        my ($one, $two, $three, $four) = ($1, $2, $3, $4);
        $left .= $one;
        $right = $four;
        my ($d1, $d2) = ($two, $three);
        my $len_d1 = length($d1);
        my $len_d2 = length($d2);
        if ($d2 == 0) {
            $d2 = 1;
        }
        $d1 = int($d1/$d2) * $d2;
        my $d1d2 = sprintf('%0'.$len_d1.'d/%0'.$len_d2.'d', $d1, $d2);
        $left .= $d1d2;
    }
    $left .= $right;
    return $left;
}

sub set_header_footer
{
    my ($header, $footer) = @_;
    $$header = <<EOF;
<head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type">
<style type="text/css">
  ol{margin:0;padding:0}
  table td,table th{padding:0}
  .c2{padding-top:0pt;padding-bottom:0pt;line-height:1.15;text-align:left}
  .c0{background-color:#ffffff;max-width:468pt;padding:72pt 72pt 72pt 72pt}
  .c1{font-family:"Courier New"}
  .title{padding-top:24pt;color:#000000;font-weight:bold;font-size:36pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  .subtitle{padding-top:18pt;color:#666666;font-size:24pt;padding-bottom:4pt;font-family:"Georgia";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}
  li{color:#000000;font-size:11pt;font-family:"Arial"}
  p{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}
  h1{padding-top:24pt;color:#000000;font-weight:bold;font-size:24pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h2{padding-top:18pt;color:#000000;font-weight:bold;font-size:18pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h3{padding-top:14pt;color:#000000;font-weight:bold;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h4{padding-top:12pt;color:#000000;font-weight:bold;font-size:12pt;padding-bottom:2pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h5{padding-top:11pt;color:#000000;font-weight:bold;font-size:11pt;padding-bottom:2pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h6{padding-top:10pt;color:#000000;font-weight:bold;font-size:10pt;padding-bottom:2pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
</style>
</head>
<body class="c0">
<p class="c2">
<span class="c1">
EOF

    $$footer = <<EOF;
</span>
</p>
</body>
</html>
EOF
}

sub rmzero_expr
{
   my ($in) = @_;
   $in =~ s{([^\d\.])0+}{$1}g;
   $in =~ s{^0+}{};
   return $in;
}
__END__
<html>
<head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type">
<style type="text/css">
  ol{margin:0;padding:0}
  table td,table th{padding:0}
  .c2{padding-top:0pt;padding-bottom:0pt;line-height:1.15;text-align:left}
  .c0{background-color:#ffffff;max-width:468pt;padding:72pt 72pt 72pt 72pt}
  .c1{font-family:"Courier New"}
  .title{padding-top:24pt;color:#000000;font-weight:bold;font-size:36pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  .subtitle{padding-top:18pt;color:#666666;font-size:24pt;padding-bottom:4pt;font-family:"Georgia";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}
  li{color:#000000;font-size:11pt;font-family:"Arial"}
  p{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}
  h1{padding-top:24pt;color:#000000;font-weight:bold;font-size:24pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h2{padding-top:18pt;color:#000000;font-weight:bold;font-size:18pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h3{padding-top:14pt;color:#000000;font-weight:bold;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h4{padding-top:12pt;color:#000000;font-weight:bold;font-size:12pt;padding-bottom:2pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h5{padding-top:11pt;color:#000000;font-weight:bold;font-size:11pt;padding-bottom:2pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
  h6{padding-top:10pt;color:#000000;font-weight:bold;font-size:10pt;padding-bottom:2pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}
</style>
</head>
<body class="c0">
<p class="c2">
<span class="c1">
9&times;88&divide;1<br><br><br><br>
9&times;88&divide;1
</span>
</p>
</body>
</html>
