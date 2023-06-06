#!/usr/bin/python
import os

os.chdir('/home/om/sb/jencomps/cron/ldap')
os.environ['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

os.system("echo '---------------------------------------' >>runlog.txt")
os.system("date >>runlog.txt")
os.system("hostname >>runlog.txt")
os.system("id >>runlog.txt")
os.system("echo '---------------------------------------' >>runlog.txt")

def main():
    home = os.environ['HOME']
    (user, password) = get_ldap_user_pass()
    chomp $password;

my $cmd = <<"__EOF__";
ldapsearch -o ldif-wrap=no \\
-LLL -z 0 -x -h ldap.purestorage.com \\
-D '$user' \\
-w '$password' \\
-E pr=2147483647/noprompt \\
-b 'DC=purestorage,DC=com' \\
'(memberOf=CN=__PureEmployees,OU=ITGroups,OU=PSGroups,DC=purestorage,DC=com)' \\
sAMAccountName \\
manager \\
userPrincipalName \\
slackUsername \\
mobile \\
physicalDeliveryOfficeName \\
streetAddress \\
title \\
givenName \\
sn \\
cn \\
name \\
mail \\
employeeID \\
employeeType \\
division \\
description \\
department \\
departmentNumber \\
uidNumber \\
gidNumber \\
unixHomeDirectory \\
startDate \\
whenCreated \\
__EOF__

my @entries = ();
my $node = {};
open RESULT, "$cmd|" or die;
while (my $line = <RESULT>) {
    if ($line eq "\n") {
        if (scalar @{$node->{body}}) {
            push @entries, $node;
        }
        $node = {};
    }
    else {
        next if($line =~ m{^\#});
        if ($line =~ m{^sAMAccountName\s*:\s*(.+?)\s*$}si) {
            $node->{name} = $1;
        }
        push @{$node->{body}}, $line;
    }
}
close RESULT;


@entries = sort {$a->{name} cmp $b->{name}} @entries;

open F, ">allusers.txt.2" or die;
for my $entry (@entries) {
    print F join '', @{$entry->{body}};
    print F "\n";
}
close F;

if (-e 'allusers.txt') {
    system 'diff -q allusers.txt allusers.txt.2';
    if ($? == 0) {
        # Same. No change
        system 'mv -f allusers.txt.2 allusers.txt.2.same';
        exit 0;
    }
    else {
        system "rm -f allusers.txt.2.same";
        my $n1 = `wc -l allusers.txt`;
        my $n2 = `wc -l allusers.txt.2`;
        $n1 =~ s{\s.*}{}s;
        $n2 =~ s{\s.*}{}s;
        if ($n1 - $n2 > 1000) {
            print "Much fewer lines than previous!\n";
            exit 1;
        }

        if (-d 'CVS') {
            system "mv -f allusers.txt.2 allusers.txt; cvs ci -mcheckpoint allusers.txt; cvs up allusers.txt";
        }
        else {
            system "rm -f allusers.txt; co -l allusers.txt; cat allusers.txt.2 >allusers.txt; rm allusers.txt.2; ci -mcheckpoint -u allusers.txt";
        }
    }
}
else {
    if (-d 'CVS') {
        system "mv allusers.txt.2 allusers.txt; cvs add allusers.txt; cvs ci -mcjeckpoint allusers.txt; cvs up allusers.txt";
    }
    else {
        system "mv allusers.txt.2 allusers.txt; ci -t-checkpoint -mcheckpoint -u allusers.txt";
    }
}

sub get_ldap_user_pass {
    my $authfile =  $ENV{HOME}.'/.ssh/ldapauth';
    open F, "<$authfile" or die;
    my $line = <F>;
    close F;
    chomp $line;
    my ($user, $pass) = $line =~ m{^(.+?)\:(.+)$};
    return ("$user\@purestorage.com", $pass);
}
