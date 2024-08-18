#include <stdio.h>
#include <stdlib.h>

void main_loop() {
    char buf[128];
    while (fgets(buf, 127, stdin) != NULL) {
        printf(buf);
    }
}

int main() {
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    main_loop();

    return 0;
}
