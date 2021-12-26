#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char** argv) {
  if (argc == 2) {
    if (strncmp(argv[1], "open", 5) == 0) {
      setuid(0);
      setgid(0);
      system("/bin/bash -x /var/root/bin/block.sh open");
    }
    else if (strncmp(argv[1], "close", 6) == 0) {
      setuid(0);
      setgid(0);
      system("/bin/bash -x /var/root/bin/block.sh close");
    }
    else if (strncmp(argv[1], "check", 6) == 0) {
      setuid(0);
      setgid(0);
      system("/bin/bash -x /var/root/bin/block.sh check");
    }
  }
  return 0;
}
