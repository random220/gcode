#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <pwd.h>
#define _POSIX_SOURCE
#include <sys/stat.h>


int goodguy(void);

int main (int argc, char** argv)
{
    setuid(0);
    setgid(0);
    if(goodguy()) {
        system("/bin/bash");
    }
    return 0;
}

int goodguy(void)
{
    char cmd[1000];
    char tmpfile_known_encrypted[40] = "/tmp/tmpfile_XXXXXX";
    char tmpfile_decrypted[40] = "/tmp/tmpfile_XXXXXX";
    FILE* f;
    char line[40];

    umask(0077);

    close(mkstemp(tmpfile_known_encrypted));
    close(mkstemp(tmpfile_decrypted));

    f = fopen(tmpfile_known_encrypted, "wt");
    fprintf(f, "U2FsdGVkX19aQXX/FPg7mUXFKq1R10oedru/JBpBg1Y=\n");
    fclose(f);

    printf("Hosta!\n\n");
    sprintf(cmd, "openssl enc -aes256 -base64 -iter 12 -in %s -out %s -d", tmpfile_known_encrypted, tmpfile_decrypted);
    printf("%s\n", cmd);
    system(cmd);

    f = fopen(tmpfile_decrypted, "rt");
    fgets(line, 40, f);
    fclose(f);

    unlink(tmpfile_known_encrypted);
    unlink(tmpfile_decrypted);

    if (strcmp ("welcome\n", line) == 0) {
        return 1;
    }
    return 0;
}


