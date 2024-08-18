#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *ptr;
int n;

void main_loop() {
    char buf[32] = {};

    while (scanf("%m[^\n]%n%*c", &ptr, &n) > 0) {
        memcpy(buf, ptr, n);
        free(ptr);
        puts(buf);
    }
}

int main() {
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    main_loop();

    return 0;
}
