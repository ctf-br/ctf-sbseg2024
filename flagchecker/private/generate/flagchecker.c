#include <stdio.h>
#include <stdint.h>

int check(const char *flag) {
    if ((*(uint64_t*)flag ^ 2795590150225918106) != 1202667998688423129)
        return 0;
    if ((*(uint32_t*)&flag[8] * 2104477190ull) != 4071967534734038930ull)
        return 0;
    if ((18032650372312564093ull / *(uint64_t*)&flag[12]) != 2)
        return 0;
    if ((18032650372312564093ull % *(uint64_t*)&flag[12]) != 3850700311778988701)
        return 0;
    if ((*(uint32_t*)&flag[20] + (uint32_t)3320943517) != 1126696674)
        return 0;
    if (flag[24] - 1 != -1)
        return 0;
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s flag_to_check\n", argv[0]);
        return 1;
    }
    if (check(argv[1])) {
        printf("flag correct\n");
        return 0;
    }
    printf("flag incorrect\n");
    return 1;
}
