use strict;
exit 1 if (!-f $ARGV[0]);
my $tarfile = "/tmp/${$}-tarfile.tgz";
my $b64file = "/tmp/${$}-b64file.tgz";
system ('tar', 'cfz', $tarfile, @ARGV);
system "openssl enc -base64 -in $tarfile -out $b64file";

print <<"EOF";
#include <stdio.h>

void printme(void)
{
    const char code[] =
    ""
    "(openssl enc -d -base64 | tar xfz -) <<\\\"__EOF__\\\"\\n"
EOF

open F, "<$b64file" or die;
while (my $line = <F>) {
    chomp $line;
    print "    \"$line\\n\"\n";
}
close F;

unlink $tarfile;
unlink $b64file;

print <<"EOF";
    "__EOF__\\n"
    ""
    ;
    printf(code);
}
EOF
