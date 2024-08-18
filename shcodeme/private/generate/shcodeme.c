#include <stdio.h>
#include <string.h>

char global_buf[2048];
int c, n;

int main() {
    char local_buf[256];

    while (1) {
        n = 0;
        while ((c = getchar()) == 0);  /* skip serial idle */
        while (1) {
            if (c == -1) {
                return 0;
            }
            if (c == '\n') {
                global_buf[n++] = 0;
                break;
            }
            else {
                global_buf[n++] = c;
            }
            c = getchar();
        }

        if (n == 1)
            break;
        
        memcpy(local_buf, global_buf, n);
        puts(local_buf);
    }

    return 0;
}
