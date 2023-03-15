#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    uid_t uid = 1002; // set user id
    gid_t gid = 1002; // set group id
    //uid = 0;
    //gid = 0;

    if (setegid(gid) != 0 || seteuid(uid) != 0) {
    //if (setgid(gid) != 0 || setuid(uid) != 0) {
        perror("setgid/setuid error");
        exit(EXIT_FAILURE);
    }
    printf("User and group identity changed successfully.\n");
    system("/usr/bin/id -a; rm -f /tmp/txt; touch /tmp/a.txt; ls -ld /tmp/a.txt");

    // Your code here
    return 0;
}
